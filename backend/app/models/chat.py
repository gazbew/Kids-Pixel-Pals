from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class ConversationType(str, enum.Enum):
    DIRECT = "DIRECT"
    GROUP = "GROUP"


class MessageType(str, enum.Enum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    SYSTEM = "system"


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    is_group = Column(Boolean, default=False)
    title = Column(String, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    members = relationship("ConversationMember", back_populates="conversation")
    messages = relationship("Message", back_populates="conversation")
    
    def __repr__(self):
        return f"<Conversation {self.id} ({'Group' if self.is_group else 'Direct'})>"


class ConversationMember(Base):
    __tablename__ = "conversation_members"
    
    conversation_id = Column(Integer, ForeignKey("conversations.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_in_convo = Column(String, default="member")  # member, admin, etc.
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="members")
    user = relationship("User")
    
    def __repr__(self):
        return f"<ConversationMember user:{self.user_id} in conv:{self.conversation_id}>"