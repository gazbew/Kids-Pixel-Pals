from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

from app.models.user import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int
    email: str
    role: UserRole


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole
    parent_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    parent_id: Optional[int] = None
    approved_by_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ParentRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    display_name: str = Field(..., min_length=2, max_length=50)


class ChildCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    display_name: str = Field(..., min_length=2, max_length=50)


class AdminApproveRequest(BaseModel):
    user_id: int