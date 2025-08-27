#!/usr/bin/env python3
"""Simple database connection test"""

import psycopg2
import os

def test_postgres_connection():
    """Test PostgreSQL connection directly"""
    try:
        # Default connection string
        conn_str = "postgresql://postgres:postgres@localhost:5432/kids_pixel_pals"
        
        # Try to connect
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        
        print(f"✅ PostgreSQL connection successful!")
        print(f"   Version: {version}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Cannot connect to PostgreSQL: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is running on localhost:5432")
        print("2. Database 'kids_pixel_pals' exists")
        print("3. User 'postgres' with password 'postgres' has access")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Testing PostgreSQL connection...")
    print("=" * 50)
    
    success = test_postgres_connection()
    
    print("=" * 50)
    if success:
        print("🎉 Database connection test passed!")
    else:
        print("💥 Database connection test failed!")
        print("\nTo set up PostgreSQL:")
        print("1. Install PostgreSQL: https://www.postgresql.org/download/")
        print("2. Create database: createdb kids_pixel_pals")
        print("3. Update .env file with your credentials")