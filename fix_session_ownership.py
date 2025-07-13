#!/usr/bin/env python3
import sqlite3

DB_PATH = "instance/app.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== FIXING SESSION OWNERSHIP ===")
    
    # Get all facilitators
    cursor.execute("SELECT id, name FROM users WHERE role = 'facilitator'")
    facilitators = cursor.fetchall()
    print(f"Found {len(facilitators)} facilitators:")
    for f in facilitators:
        print(f"  ID {f[0]}: {f[1]}")
    
    # Get all sessions
    cursor.execute("SELECT id, facilitator_id FROM sessions")
    sessions = cursor.fetchall()
    print(f"\nFound {len(sessions)} sessions")
    
    # Reassign sessions round-robin to ensure proper ownership
    print("\nReassigning sessions to facilitators...")
    for idx, (session_id, old_fac_id) in enumerate(sessions):
        # Assign to facilitator in round-robin fashion
        new_fac_id = facilitators[idx % len(facilitators)][0]
        
        cursor.execute("UPDATE sessions SET facilitator_id = ? WHERE id = ?", (new_fac_id, session_id))
        print(f"Session {session_id}: {old_fac_id} → {new_fac_id}")
    
    conn.commit()
    
    # Verify the fix
    print("\n=== VERIFICATION ===")
    for fac_id, fac_name in facilitators:
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE facilitator_id = ?", (fac_id,))
        count = cursor.fetchone()[0]
        print(f"{fac_name} (ID: {fac_id}): {count} sessions")
    
    conn.close()
    print("\n✅ Session ownership fixed!")

if __name__ == "__main__":
    main() 