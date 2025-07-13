#!/usr/bin/env python3
import sqlite3

DB_PATH = "instance/app.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=== SESSION OWNERSHIP CHECK ===")
    
    # Get all facilitators
    cursor.execute("SELECT id, name, email FROM users WHERE role = 'facilitator'")
    facilitators = cursor.fetchall()
    
    print(f"\nFound {len(facilitators)} facilitators:")
    for f in facilitators:
        print(f"  ID {f[0]}: {f[1]} ({f[2]})")
    
    # Check sessions for each facilitator
    for fac_id, fac_name, fac_email in facilitators:
        cursor.execute("""
            SELECT id, start_time, end_time, max_participants 
            FROM sessions 
            WHERE facilitator_id = ?
        """, (fac_id,))
        sessions = cursor.fetchall()
        
        print(f"\n📋 {fac_name} (ID: {fac_id}) has {len(sessions)} sessions:")
        for session in sessions:
            print(f"  Session {session[0]}: {session[1]} to {session[2]} (max: {session[3]})")
    
    # Check for sessions without facilitators
    cursor.execute("SELECT COUNT(*) FROM sessions WHERE facilitator_id IS NULL")
    null_count = cursor.fetchone()[0]
    if null_count > 0:
        print(f"\n⚠️  WARNING: {null_count} sessions have no facilitator assigned!")
    
    conn.close()

if __name__ == "__main__":
    main() 