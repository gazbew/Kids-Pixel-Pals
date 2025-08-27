from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, RedisDsn, Field
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: PostgresDsn = Field(
        default="postgresql://postgres:postgres@localhost:5432/kids_pixel_pals"
    )
    
    # Redis
    redis_url: RedisDsn = Field(default="redis://localhost:6379/0")
    
    # JWT
    jwt_secret_key: str = Field(
        default="change_this_in_production_with_secure_random_key",
        description="Secret key for JWT token signing"
    )
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=15)
    refresh_token_expire_days: int = Field(default=7)
    
    # Security
    encryption_key: str = Field(
        default="change_this_32_byte_key_for_production",
        description="32-byte key for AES-256 encryption"
    )
    
    # CORS
    cors_origins: list[str] = Field(default=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Environment
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()