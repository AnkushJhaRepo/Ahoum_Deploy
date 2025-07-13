#!/usr/bin/env python3
"""
Create a facilitator user directly
"""

import sqlite3
from datetime import datetime

DB_PATH = "instance/app.db"

def create_facilitator():
    """Create a new facilitator user"""
    
    print("Creating new facilitator user...")
    print("=" * 50)
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create facilitator user
        email = "facilitator@test.com"
        password = "facilitator123"
        name = "Test Facilitator"
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"User {email} already exists!")
            print(f"   User ID: {existing[0]}")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   Role: facilitator")
        else:
            # Insert new user
            cursor.execute("""
                INSERT INTO users (name, email, password_hash, role, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, email, password, 'facilitator', datetime.utcnow(), datetime.utcnow()))
            
            # Get the user ID
            user_id = cursor.lastrowid
            
            # Commit changes
            conn.commit()
            
            print(f"✅ New facilitator user created successfully!")
            print(f"   User ID: {user_id}")
            print(f"   Name: {name}")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   Role: facilitator")
        
        print()
        print("You can now login to the facilitator dashboard with these credentials.")
        print("Dashboard URL: http://127.0.0.1:5000/api/facilitator/dashboard-page")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating facilitator user: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_facilitator() 