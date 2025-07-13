#!/usr/bin/env python3
"""
Test script to check session ownership and facilitator details
"""

import sys
import os
import requests
import sqlite3

BASE_URL = "http://localhost:5000"
DB_PATH = "instance/app.db"

def test_session_ownership():
    """Test session ownership and facilitator details"""
    
    print("Testing Session Ownership...")
    print("=" * 50)
    
    try:
        # Connect to database directly
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # First, let's check the facilitator user details
        print("1. Checking facilitator user details...")
        
        cursor.execute("SELECT id, name, email, role FROM users WHERE email = ?", 
                      ("facilitator_gvt2zb@test.com",))
        facilitator = cursor.fetchone()
        
        if facilitator:
            facilitator_id, name, email, role = facilitator
            print(f"   Facilitator ID: {facilitator_id}")
            print(f"   Facilitator Name: {name}")
            print(f"   Facilitator Email: {email}")
            print(f"   Role: {role}")
        else:
            print("   ❌ Facilitator user not found")
            return
        
        # Check session 58
        print("\n2. Checking session 58 details...")
        cursor.execute("SELECT id, event_id, facilitator_id, time, location FROM sessions WHERE id = ?", (58,))
        session_58 = cursor.fetchone()
        
        if session_58:
            session_id, event_id, session_facilitator_id, time, location = session_58
            print(f"   Session ID: {session_id}")
            print(f"   Event ID: {event_id}")
            print(f"   Facilitator ID: {session_facilitator_id}")
            print(f"   Time: {time}")
            print(f"   Location: {location}")
            
            # Check if the session belongs to our facilitator
            if session_facilitator_id == facilitator_id:
                print("   ✅ Session 58 belongs to our facilitator")
            else:
                print("   ❌ Session 58 does NOT belong to our facilitator")
                print(f"   Expected: {facilitator_id}, Got: {session_facilitator_id}")
        else:
            print("   ❌ Session 58 not found")
            return
        
        # Check all sessions for our facilitator
        print("\n3. Checking all sessions for our facilitator...")
        cursor.execute("SELECT id, location, time FROM sessions WHERE facilitator_id = ?", (facilitator_id,))
        facilitator_sessions = cursor.fetchall()
        
        print(f"   Total sessions for facilitator: {len(facilitator_sessions)}")
        
        for session in facilitator_sessions:
            session_id, location, time = session
            print(f"   Session {session_id}: {location} at {time}")
        
        # Check if session 58 is in the list
        session_58_in_list = any(s[0] == 58 for s in facilitator_sessions)
        if session_58_in_list:
            print("   ✅ Session 58 is in facilitator's sessions")
        else:
            print("   ❌ Session 58 is NOT in facilitator's sessions")
        
        # Check what facilitator actually owns session 58
        if session_facilitator_id != facilitator_id:
            print(f"\n4. Checking who actually owns session 58...")
            cursor.execute("SELECT id, name, email, role FROM users WHERE id = ?", (session_facilitator_id,))
            actual_owner = cursor.fetchone()
            if actual_owner:
                owner_id, owner_name, owner_email, owner_role = actual_owner
                print(f"   Session 58 is owned by: {owner_name} ({owner_email}) - Role: {owner_role}")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_session_ownership() 