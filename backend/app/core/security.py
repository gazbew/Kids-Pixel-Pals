from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import base64
import os

from .config import settings


# Password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Encryption for sensitive data
encryption_key = base64.urlsafe_b64encode(settings.encryption_key.encode()[:32].ljust(32))
cipher_suite = Fernet(encryption_key)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None


def encrypt_data(data: str) -> tuple[bytes, bytes]:
    """Encrypt sensitive data with AES-256"""
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data


def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypt sensitive data"""
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()