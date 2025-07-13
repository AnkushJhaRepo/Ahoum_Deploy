#!/usr/bin/env python3
import sqlite3
from datetime import datetime, timedelta

DB_PATH = 'instance/app.db'

def assign_session_to_facilitator():
    """Assign a session to the facilitator for testing"""
    print("=== Assigning Session to Facilitator ===\n")
    
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
        
        # Check if there are any events
        cursor.execute("SELECT id, title FROM events LIMIT 1")
        event = cursor.fetchone()
        
        if not event:
            print("❌ No events found in database")
            return
        
        event_id = event[0]
        print(f"✅ Using event: {event[1]} (ID: {event_id})")
        
        # Check if there are any existing sessions
        cursor.execute("SELECT id, time, location, facilitator_id FROM sessions WHERE event_id = ?", (event_id,))
        existing_sessions = cursor.fetchall()
        
        if existing_sessions:
            print(f"✅ Found {len(existing_sessions)} existing sessions")
            
            # Find a session without a facilitator or assign to an existing one
            unassigned_session = None
            for session in existing_sessions:
                if session[3] is None:  # No facilitator assigned
                    unassigned_session = session
                    break
            
            if unassigned_session:
                session_id = unassigned_session[0]
                print(f"✅ Found unassigned session ID: {session_id}")
                
                # Assign this session to the facilitator
                cursor.execute("UPDATE sessions SET facilitator_id = ? WHERE id = ?", (facilitator_id, session_id))
                conn.commit()
                print(f"✅ Assigned session {session_id} to facilitator")
                
                # Display session details
                cursor.execute("SELECT time, location FROM sessions WHERE id = ?", (session_id,))
                session_details = cursor.fetchone()
                print(f"   Time: {session_details[0]}")
                print(f"   Location: {session_details[1]}")
                
            else:
                print("ℹ️  All sessions are already assigned. Creating a new session...")
                create_new_session(cursor, conn, event_id, facilitator_id)
        else:
            print("ℹ️  No sessions found. Creating a new session...")
            create_new_session(cursor, conn, event_id, facilitator_id)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        conn.close()

def create_new_session(cursor, conn, event_id, facilitator_id):
    """Create a new session for the facilitator"""
    # Create a session time in the future (tomorrow)
    tomorrow = datetime.now() + timedelta(days=1)
    session_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
    
    session_data = {
        'event_id': event_id,
        'facilitator_id': facilitator_id,
        'time': session_time.isoformat(),
        'location': 'Test Room 101',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    cursor.execute("""
        INSERT INTO sessions (event_id, facilitator_id, time, location, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session_data['event_id'],
        session_data['facilitator_id'],
        session_data['time'],
        session_data['location'],
        session_data['created_at'],
        session_data['updated_at']
    ))
    
    session_id = cursor.lastrowid
    conn.commit()
    
    print(f"✅ Created new session ID: {session_id}")
    print(f"   Time: {session_data['time']}")
    print(f"   Location: {session_data['location']}")

if __name__ == "__main__":
    assign_session_to_facilitator() 