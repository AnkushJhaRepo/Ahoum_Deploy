#!/usr/bin/env python3
"""
Check database structure
"""

import sqlite3

DB_PATH = "instance/app.db"

def check_db():
    """Check database structure"""
    
    print("Checking database structure...")
    print("=" * 50)
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("Users table columns:")
        for col in columns:
            print(f"   {col[1]} ({col[2]})")
        
        # Check existing users
        cursor.execute("SELECT id, name, email, role FROM users LIMIT 5")
        users = cursor.fetchall()
        
        print(f"\nExisting users (first 5):")
        for user in users:
            print(f"   ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Role: {user[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    check_db() 