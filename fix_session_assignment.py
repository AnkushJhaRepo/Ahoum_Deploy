#!/usr/bin/env python3
import sqlite3

DB_PATH = 'instance/app.db'

def fix_session_assignment():
    """Fix the session assignment to the facilitator"""
    print("=== Fixing Session Assignment ===\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get facilitator user ID
        cursor.execute("SELECT id FROM users WHERE email = ?", ('facilitator_gvt2zb@test.com',))
        facilitator = cursor.fetchone()
        
        if not facilitator:
            print("❌ Facilitator user not found")
            return
        
        facilitator_id = facilitator[0]
        print(f"✅ Found facilitator with ID: {facilitator_id}")
        
        # Check the session we just created
        cursor.execute("SELECT id, event_id, facilitator_id, time, location FROM sessions WHERE id = 58")
        session = cursor.fetchone()
        
        if not session:
            print("❌ Session 58 not found")
            return
        
        session_id, event_id, current_facilitator_id, time, location = session
        print(f"✅ Found session {session_id}")
        print(f"   Event ID: {event_id}")
        print(f"   Current Facilitator ID: {current_facilitator_id}")
        print(f"   Time: {time}")
        print(f"   Location: {location}")
        
        if current_facilitator_id != facilitator_id:
            print(f"❌ Session is assigned to facilitator {current_facilitator_id}, not {facilitator_id}")
            
            # Fix the assignment
            cursor.execute("UPDATE sessions SET facilitator_id = ? WHERE id = ?", (facilitator_id, session_id))
            conn.commit()
            print(f"✅ Fixed: Session {session_id} now assigned to facilitator {facilitator_id}")
        else:
            print(f"✅ Session is already correctly assigned to facilitator {facilitator_id}")
        
        # Verify the fix
        cursor.execute("SELECT facilitator_id FROM sessions WHERE id = ?", (session_id,))
        updated_session = cursor.fetchone()
        print(f"✅ Verification: Session {session_id} facilitator_id = {updated_session[0]}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_session_assignment() 