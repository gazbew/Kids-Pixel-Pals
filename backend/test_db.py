#!/usr/bin/env python3
"""Test database connection script"""

import sys
from sqlalchemy import text
from app.core.database import engine, SessionLocal

def test_database_connection():
    """Test if database connection works"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Database connection successful! PostgreSQL version: {version}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_session():
    """Test database session"""
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1"))
        db.close()
        print("✅ Database session test successful!")
        return True
    except Exception as e:
        print(f"❌ Database session test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    
    connection_ok = test_database_connection()
    session_ok = test_session()
    
    if connection_ok and session_ok:
        print("\n🎉 All database tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Database tests failed!")
        sys.exit(1)