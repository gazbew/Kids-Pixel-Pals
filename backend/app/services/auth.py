from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import timedelta

from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.models.user import User, UserRole, Profile
from app.schemas.auth import UserCreate, ParentRegisterRequest, ChildCreateRequest
from app.schemas.profile import ProfileCreate


class AuthService:
    @staticmethod
    def register_parent(db: Session, request: ParentRegisterRequest) -> User:
        """Register a new parent account (requires admin approval)"""
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        try:
            # Create user
            user = User(
                email=request.email,
                password_hash=get_password_hash(request.password),
                role=UserRole.PARENT,
                approved_by_admin=False  # Requires admin approval
            )
            db.add(user)
            db.flush()  # Get user ID for profile
            
            # Create profile
            profile = Profile(
                user_id=user.id,
                display_name=request.display_name
            )
            db.add(profile)
            
            db.commit()
            db.refresh(user)
            return user
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed"
            )

    @staticmethod
    def create_child_account(db: Session, parent_user: User, request: ChildCreateRequest) -> User:
        """Create a child account (parent must be approved)"""
        if not parent_user.approved_by_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Parent account requires admin approval before creating child accounts"
            )
        
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == request.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        try:
            # Create child user
            user = User(
                email=request.email,
                password_hash=get_password_hash(request.password),
                role=UserRole.CHILD,
                parent_id=parent_user.id,
                approved_by_admin=True  # Children are automatically approved
            )
            db.add(user)
            db.flush()
            
            # Create profile
            profile = Profile(
                user_id=user.id,
                display_name=request.display_name
            )
            db.add(profile)
            
            db.commit()
            db.refresh(user)
            return user
            
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Child account creation failed"
            )

    @staticmethod
    def login(db: Session, email: str, password: str):
        """Authenticate user and return tokens"""
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check if parent requires approval
        if user.role == UserRole.PARENT and not user.approved_by_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Parent account pending admin approval"
            )
        
        # Create tokens
        token_data = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role.value
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": user
        }

    @staticmethod
    def approve_parent(db: Session, user_id: int) -> User:
        """Approve a parent account (admin only)"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.role != UserRole.PARENT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only approve parent accounts"
            )
        
        user.approved_by_admin = True
        db.commit()
        db.refresh(user)
        return user