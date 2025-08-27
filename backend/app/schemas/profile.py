from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProfileBase(BaseModel):
    display_name: str = Field(..., min_length=2, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)


class ProfileCreate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    avatar_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    display_name: Optional[str] = Field(None, min_length=2, max_length=50)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None


class GameCredentialBase(BaseModel):
    game_name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=1, max_length=100)


class GameCredentialCreate(GameCredentialBase):
    password: str = Field(..., min_length=1, max_length=100)


class GameCredentialResponse(GameCredentialBase):
    id: int
    profile_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True