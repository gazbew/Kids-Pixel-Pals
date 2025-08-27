from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    PARENT = "PARENT"
    CHILD = "CHILD"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_by_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    children = relationship("User", back_populates="parent", remote_side=[id])
    parent = relationship("User", back_populates="children", remote_side=[parent_id])
    profile = relationship("Profile", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    game_credentials = relationship("GameCredential", back_populates="profile")
    
    def __repr__(self):
        return f"<Profile {self.display_name}>"


class GameCredential(Base):
    __tablename__ = "game_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    game_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password_ciphertext = Column(String, nullable=False)  # Encrypted password
    iv = Column(String, nullable=False)  # Initialization vector for encryption
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("Profile", back_populates="game_credentials")
    
    def __repr__(self):
        return f"<GameCredential {self.game_name} for {self.username}>"