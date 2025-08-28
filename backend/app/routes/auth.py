from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import timedelta

from app.core.database import get_db
from app.core.security import get_password_hash
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token, blacklist_token
from app.core.config import settings
from app.dependencies.auth import get_current_user, require_admin
from app.models.user import User, UserRole
from app.schemas.auth import (
    Token, LoginRequest, ParentRegisterRequest, 
    ChildCreateRequest, AdminApproveRequest, UserResponse,
    PasswordResetRequest, PasswordResetConfirm, ChangePasswordRequest,
    UserListResponse, UserFilter
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
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    
    # Verify refresh token
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user from database
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Blacklist the used refresh token
    blacklist_token(refresh_token, timedelta(days=settings.refresh_token_expire_days))
    
    # Create new tokens
    token_data = {
        "user_id": user.id,
        "email": user.email,
        "role": user.role.value
    }
    
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)
    
    # Set new refresh token as httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60  # 7 days
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user)
    }


@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_user)
):
    """Logout and blacklist tokens"""
    # Get access token from Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        access_token = auth_header[7:]
        # Blacklist access token
        blacklist_token(access_token)
    
    # Get and blacklist refresh token
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        blacklist_token(refresh_token, timedelta(days=settings.refresh_token_expire_days))
    
    # Clear refresh token cookie
    response.delete_cookie("refresh_token")
    
    return {"message": "Logged out successfully"}


@router.post("/password/reset/request")
def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset (sends email with reset token)"""
    AuthService.request_password_reset(db, request.email)
    return {"message": "Password reset instructions sent to email"}


@router.post("/password/reset/confirm")
def confirm_password_reset(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Confirm password reset with token"""
    AuthService.confirm_password_reset(db, request.token, request.new_password)
    return {"message": "Password reset successfully"}


@router.post("/password/change")
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password for authenticated user"""
    AuthService.change_password(db, current_user, request.current_password, request.new_password)
    return {"message": "Password changed successfully"}


# Admin endpoints for user management
@router.get("/admin/users", response_model=UserListResponse)
def list_users(
    filter: UserFilter = Depends(),
    skip: int = 0,
    limit: int = 100,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """List users with filtering (admin only)"""
    query = db.query(User)
    
    if filter.role:
        query = query.filter(User.role == filter.role)
    if filter.approved is not None:
        query = query.filter(User.approved_by_admin == filter.approved)
    if filter.search:
        query = query.filter(User.email.ilike(f"%{filter.search}%"))
    
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    return UserListResponse(users=users, total=total)


@router.get("/admin/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Get user details (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/admin/users/{user_id}")
def delete_user(
    user_id: int,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deleting admin accounts
    if user.role == UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete admin accounts"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}