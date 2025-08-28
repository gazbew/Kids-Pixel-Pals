from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import json
import asyncio

from app.core.database import get_db
from app.core.websocket import manager, websocket_auth
from app.models.user import User

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time communication"""
    user = await websocket_auth(websocket, db)
    if not user:
        return
    
    await manager.connect(websocket, user.id)
    
    try:
        while True:
            # Receive and handle messages
            data = await websocket.receive_json()
            
            if data["type"] == "message":
                # Handle new message
                await handle_new_message(data, user, db)
            
            elif data["type"] == "typing":
                # Handle typing indicator
                await handle_typing(data, user, db)
            
            elif data["type"] == "ping":
                # Respond to ping
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user.id)


async def handle_new_message(data: dict, user: User, db: Session):
    """Handle incoming message and broadcast to conversation"""
    from app.models.message import Message
    from app.models.chat import ConversationMember
    
    conversation_id = data["conversation_id"]
    content = data["content"]
    message_type = data.get("message_type", "text")
    
    # Verify user is member of conversation
    member = db.query(ConversationMember).filter(
        ConversationMember.conversation_id == conversation_id,
        ConversationMember.user_id == user.id
    ).first()
    
    if not member:
        return
    
    # Create message in database
    new_message = Message(
        conversation_id=conversation_id,
        sender_id=user.id,
        type=message_type,
        content=content,
        media_url=data.get("media_url")
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    # Prepare broadcast message
    broadcast_msg = {
        "type": "message",
        "message_id": new_message.id,
        "conversation_id": conversation_id,
        "sender_id": user.id,
        "sender_name": user.display_name,
        "content": content,
        "message_type": message_type,
        "media_url": data.get("media_url"),
        "timestamp": new_message.created_at.isoformat()
    }
    
    # Broadcast to all conversation members
    await manager.broadcast_to_conversation(conversation_id, broadcast_msg, db)


async def handle_typing(data: dict, user: User, db: Session):
    """Handle typing indicators"""
    from app.models.chat import ConversationMember
    
    conversation_id = data["conversation_id"]
    is_typing = data["is_typing"]
    
    # Verify user is member of conversation
    member = db.query(ConversationMember).filter(
        ConversationMember.conversation_id == conversation_id,
        ConversationMember.user_id == user.id
    ).first()
    
    if not member:
        return
    
    # Set typing indicator in Redis
    key = f"typing:{conversation_id}:{user.id}"
    if is_typing:
        manager.redis_client.setex(key, 3, "typing")
    else:
        manager.redis_client.delete(key)
    
    # Broadcast typing status to other conversation members
    typing_msg = {
        "type": "typing",
        "conversation_id": conversation_id,
        "user_id": user.id,
        "user_name": user.display_name,
        "is_typing": is_typing
    }
    
    # Get all members except current user
    members = db.query(ConversationMember.user_id).filter(
        ConversationMember.conversation_id == conversation_id,
        ConversationMember.user_id != user.id
    ).all()
    
    for member in members:
        await manager.broadcast_to_user(member[0], typing_msg)


# Startup event will be handled in main.py