#!/usr/bin/env python3
"""
Create a facilitator user with properly hashed password
"""

import sys
import os
import sqlite3
from datetime import datetime
import bcrypt

# Add the main_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'main_app'))

DB_PATH = "instance/app.db"

def create_facilitator():
    """Create a new facilitator user with hashed password"""
    
    print("Creating new facilitator user with properly hashed password...")
    print("=" * 60)
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create facilitator user
        email = "facilitator@test.com"
        password = "facilitator123"
        name = "Test Facilitator"
        
        # Hash the password using bcrypt (same as AuthService)
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        hashed_password = hashed.decode('utf-8')
        
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Hashed password: {hashed_password[:20]}...")
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"User {email} already exists! Updating...")
            cursor.execute("""
                UPDATE users 
                SET password = ?, role = 'facilitator'
                WHERE email = ?
            """, (hashed_password, email))
        else:
            print(f"Creating new user {email}...")
            cursor.execute("""
                INSERT INTO users (name, email, password, role, created_at)
                VALUES (?, ?, ?, 'facilitator', ?)
            """, (name, email, hashed_password, datetime.utcnow()))
        
        # Commit changes
        conn.commit()
        
        # Get the user ID
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_id = cursor.fetchone()[0]
        
        print(f"✅ Facilitator user created/updated successfully!")
        print(f"User ID: {user_id}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Role: facilitator")
        
        # Test the password hash
        test_result = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        print(f"Password verification test: {'✅ PASS' if test_result else '❌ FAIL'}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating facilitator: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    create_facilitator() 