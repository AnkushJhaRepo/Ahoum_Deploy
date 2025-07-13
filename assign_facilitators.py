#!/usr/bin/env python3
import sqlite3

DB_PATH = "instance/app.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all facilitators
    cursor.execute("SELECT id, name FROM users WHERE role = 'facilitator'")
    facilitators = cursor.fetchall()
    print(f"Found {len(facilitators)} facilitators:")
    for f in facilitators:
        print(f"  {f}")
    
    if not facilitators:
        print("No facilitators found!")
        return
    
    # Get all sessions
    cursor.execute("SELECT id, facilitator_id FROM sessions")
    sessions = cursor.fetchall()
    print(f"\nFound {len(sessions)} sessions:")
    for s in sessions:
        print(f"  Session {s[0]}: facilitator_id = {s[1]}")
    
    if not sessions:
        print("No sessions found!")
        return
    
    # Assign facilitators round-robin
    print("\nAssigning facilitators to sessions...")
    for idx, (session_id, old_fac_id) in enumerate(sessions):
        fac_id = facilitators[idx % len(facilitators)][0]
        cursor.execute("UPDATE sessions SET facilitator_id = ? WHERE id = ?", (fac_id, session_id))
        print(f"Session {session_id} assigned to facilitator {fac_id}")
    
    conn.commit()
    
    print("\nFinal assignment:")
    cursor.execute("SELECT id, facilitator_id FROM sessions")
    for s in cursor.fetchall():
        print(f"  Session {s[0]}: facilitator_id = {s[1]}")
    
    conn.close()

if __name__ == "__main__":
    main() 