from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User, UserRole
from app.schemas.auth import (
    Token, LoginRequest, ParentRegisterRequest, 
    ChildCreateRequest, AdminApproveRequest, UserResponse
)
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/parent/register", response_model=UserResponse)
def register_parent(
    request: ParentRegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new parent account (requires admin approval)"""
    user = AuthService.register_parent(db, request)
    return user


@router.post("/login")
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """Login and get access/refresh tokens"""
    result = AuthService.login(db, request.email, request.password)
    
    # Set refresh token as httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60  # 7 days
    )
    
    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"],
        "user": UserResponse.from_orm(result["user"])
    }


@router.post("/child", response_model=UserResponse)
def create_child_account(
    request: ChildCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a child account (parent must be approved)"""
    if current_user.role != UserRole.PARENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can create child accounts"
        )
    
    child_user = AuthService.create_child_account(db, current_user, request)
    return child_user


@router.post("/admin/approve", response_model=UserResponse)
def approve_parent(
    request: AdminApproveRequest,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Approve a parent account (admin only)"""
    approved_user = AuthService.approve_parent(db, request.user_id)
    return approved_user


@router.post("/refresh")
def refresh_token(
    response: Response,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    # Implementation for token refresh
    # This would verify the refresh token from cookies and issue new access token
    pass


@router.post("/logout")
def logout(response: Response):
    """Logout and clear refresh token"""
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}