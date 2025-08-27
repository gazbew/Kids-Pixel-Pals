from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)  # e.g., "user_created", "account_approved"
    entity_type = Column(String, nullable=False)  # e.g., "user", "conversation"
    entity_id = Column(Integer, nullable=True)  # ID of the affected entity
    before_json = Column(JSON, nullable=True)  # State before action
    after_json = Column(JSON, nullable=True)  # State after action
    ip = Column(String, nullable=True)  # IP address of actor
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    actor = relationship("User")
    
    def __repr__(self):
        return f"<AuditLog {self.action} by user:{self.actor_id}>"