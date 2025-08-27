from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from .chat import MessageType


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(MessageType), nullable=False, default=MessageType.TEXT)
    content = Column(Text, nullable=True)  # For text messages
    media_url = Column(String, nullable=True)  # For audio/image messages
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User")
    
    def __repr__(self):
        return f"<Message {self.id} ({self.type}) in conv:{self.conversation_id}>"