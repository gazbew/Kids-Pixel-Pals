from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
import redis
import asyncio
from typing import Dict, List, Optional

from .database import get_db
from .config import settings
from .security import verify_token
from app.models.user import User


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.redis_client = redis.from_url(str(settings.redis_url))
        self.pubsub = self.redis_client.pubsub()
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        
        # Set user as online
        self.redis_client.setex(f"ws_online:{user_id}", 300, "online")
        
        # Subscribe to user's personal channel
        await self._subscribe_to_user_channel(user_id)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                # Remove online status if no more connections
                self.redis_client.delete(f"ws_online:{user_id}")
    
    async def _subscribe_to_user_channel(self, user_id: int):
        """Subscribe to Redis channel for user-specific messages"""
        self.pubsub.subscribe(f"user:{user_id}")
    
    async def broadcast_to_user(self, user_id: int, message: dict):
        """Send message to specific user"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    self.disconnect(connection, user_id)
    
    async def broadcast_to_conversation(self, conversation_id: int, message: dict, db: Session):
        """Broadcast message to all users in a conversation"""
        # Get all members of the conversation
        from app.models.chat import ConversationMember
        members = db.query(ConversationMember.user_id).filter(
            ConversationMember.conversation_id == conversation_id
        ).all()
        
        for member in members:
            user_id = member[0]
            await self.broadcast_to_user(user_id, message)
    
    async def send_personal_message(self, message: dict):
        """Send message via Redis pub/sub"""
        user_id = message.get("user_id")
        if user_id:
            self.redis_client.publish(f"user:{user_id}", json.dumps(message))
    
    async def handle_redis_messages(self):
        """Handle incoming Redis messages"""
        while True:
            try:
                message = self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    data = json.loads(message["data"])
                    user_id = data.get("user_id")
                    if user_id:
                        await self.broadcast_to_user(int(user_id), data)
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Redis message handling error: {e}")
                await asyncio.sleep(1)


# Global connection manager
manager = ConnectionManager()


def get_user_from_token(token: str, db: Session) -> Optional[User]:
    """Verify JWT token and get user"""
    payload = verify_token(token)
    if not payload:
        return None
    
    user_id = payload.get("user_id")
    if not user_id:
        return None
    
    return db.query(User).filter(User.id == user_id).first()


async def websocket_auth(websocket: WebSocket, db: Session):
    """Authenticate WebSocket connection"""
    try:
        # Get token from query parameter
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None
        
        user = get_user_from_token(token, db)
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None
        
        return user
    except Exception as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return None