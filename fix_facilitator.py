#!/usr/bin/env python3
"""
Fix facilitator user password
"""

import sqlite3
from datetime import datetime

DB_PATH = "instance/app.db"

def fix_facilitator():
    """Fix facilitator user password"""
    
    print("Fixing facilitator user...")
    print("=" * 50)
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Update the existing facilitator user
        email = "facilitator@test.com"
        password = "facilitator123"  # Plain text password
        
        # Update user
        cursor.execute("""
            UPDATE users 
            SET password = ?, role = 'facilitator', updated_at = ?
            WHERE email = ?
        """, (password, datetime.utcnow(), email))
        
        # Check if update was successful
        cursor.execute("SELECT id, name, email, role FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            print(f"✅ Facilitator user updated successfully!")
            print(f"   User ID: {user[0]}")
            print(f"   Name: {user[1]}")
            print(f"   Email: {user[2]}")
            print(f"   Role: {user[3]}")
            print(f"   Password: {password}")
        else:
            print("❌ User not found!")
        
        # Commit changes
        conn.commit()
        
        print()
        print("You can now login to the facilitator dashboard with these credentials.")
        print("Dashboard URL: http://127.0.0.1:5000/api/facilitator/dashboard-page")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_facilitator() 