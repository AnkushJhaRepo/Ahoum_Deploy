#!/usr/bin/env python3
"""
Create a new facilitator user
"""

import sys
import os
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
        
        # Generate unique email
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        email = f"facilitator_{timestamp}@test.com"
        password = "facilitator123"
        name = f"Facilitator {timestamp}"
        
        # Insert new user
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, role, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, password, 'facilitator', datetime.utcnow(), datetime.utcnow()))
        
        # Get the user ID
        user_id = cursor.lastrowid
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print(f"✅ New facilitator user created successfully!")
        print(f"   User ID: {user_id}")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"   Role: facilitator")
        print()
        print("You can now login to the facilitator dashboard with these credentials.")
        print("Dashboard URL: http://127.0.0.1:5000/api/facilitator/dashboard-page")
        
    except Exception as e:
        print(f"❌ Error creating facilitator user: {str(e)}")

if __name__ == "__main__":
    create_facilitator() 