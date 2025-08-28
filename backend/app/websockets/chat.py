from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import json
import asyncio
from typing import Dict, List

from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.models.chat import Conversation, ConversationMember
from app.models.message import Message


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.conversation_subscriptions: Dict[int, List[int]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"User {user_id} connected")

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        # Remove user from all conversation subscriptions
        for conv_id, users in self.conversation_subscriptions.items():
            if user_id in users:
                users.remove(user_id)
        print(f"User {user_id} disconnected")

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except:
                self.disconnect(user_id)

    async def broadcast_to_conversation(self, message: dict, conversation_id: int, exclude_user_id: int = None):
        if conversation_id in self.conversation_subscriptions:
            for user_id in self.conversation_subscriptions[conversation_id]:
                if user_id != exclude_user_id and user_id in self.active_connections:
                    try:
                        await self.active_connections[user_id].send_json(message)
                    except:
                        self.disconnect(user_id)

    def subscribe_to_conversation(self, user_id: int, conversation_id: int):
        if conversation_id not in self.conversation_subscriptions:
            self.conversation_subscriptions[conversation_id] = []
        if user_id not in self.conversation_subscriptions[conversation_id]:
            self.conversation_subscriptions[conversation_id].append(user_id)

    def unsubscribe_from_conversation(self, user_id: int, conversation_id: int):
        if conversation_id in self.conversation_subscriptions:
            if user_id in self.conversation_subscriptions[conversation_id]:
                self.conversation_subscriptions[conversation_id].remove(user_id)


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    """WebSocket endpoint for real-time chat"""
    
    # Verify authentication token
    payload = verify_token(token)
    if not payload:
        await websocket.close(code=1008)
        return
    
    user_id = payload["user_id"]
    
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "subscribe":
                # Subscribe to conversation
                conversation_id = data["conversation_id"]
                
                # Verify user has access to conversation
                member = db.query(ConversationMember).filter(
                    ConversationMember.conversation_id == conversation_id,
                    ConversationMember.user_id == user_id
                ).first()
                
                if not member:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Access denied to conversation"
                    })
                    continue
                
                manager.subscribe_to_conversation(user_id, conversation_id)
                await websocket.send_json({
                    "type": "subscribed",
                    "conversation_id": conversation_id
                })
                
            elif data["type"] == "message":
                # Send message to conversation
                conversation_id = data["conversation_id"]
                content = data["content"]
                
                # Verify user has access to conversation
                member = db.query(ConversationMember).filter(
                    ConversationMember.conversation_id == conversation_id,
                    ConversationMember.user_id == user_id
                ).first()
                
                if not member:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Access denied to conversation"
                    })
                    continue
                
                # Create message in database
                message = Message(
                    conversation_id=conversation_id,
                    sender_id=user_id,
                    type="text",
                    content=content
                )
                db.add(message)
                db.commit()
                db.refresh(message)
                
                # Get sender info
                sender = db.query(User).filter(User.id == user_id).first()
                
                # Broadcast message to all subscribers
                message_data = {
                    "type": "message",
                    "id": message.id,
                    "conversation_id": conversation_id,
                    "sender_id": user_id,
                    "sender_display_name": sender.display_name if sender else "Unknown",
                    "content": content,
                    "created_at": message.created_at.isoformat(),
                    "timestamp": message.created_at.isoformat()
                }
                
                await manager.broadcast_to_conversation(message_data, conversation_id, user_id)
                
            elif data["type"] == "typing":
                # Typing indicator
                conversation_id = data["conversation_id"]
                is_typing = data["is_typing"]
                
                # Verify user has access to conversation
                member = db.query(ConversationMember).filter(
                    ConversationMember.conversation_id == conversation_id,
                    ConversationMember.user_id == user_id
                ).first()
                
                if not member:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Access denied to conversation"
                    })
                    continue
                
                # Get sender info
                sender = db.query(User).filter(User.id == user_id).first()
                
                # Broadcast typing indicator
                typing_data = {
                    "type": "typing",
                    "conversation_id": conversation_id,
                    "user_id": user_id,
                    "user_display_name": sender.display_name if sender else "Unknown",
                    "is_typing": is_typing
                }
                
                await manager.broadcast_to_conversation(typing_data, conversation_id, user_id)
                
            elif data["type"] == "online":
                # Online status update
                is_online = data["is_online"]
                
                # Broadcast online status to all conversations user is in
                user_conversations = db.query(ConversationMember.conversation_id).filter(
                    ConversationMember.user_id == user_id
                ).all()
                
                online_data = {
                    "type": "online",
                    "user_id": user_id,
                    "is_online": is_online
                }
                
                for conv in user_conversations:
                    await manager.broadcast_to_conversation(online_data, conv[0], user_id)
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(user_id)