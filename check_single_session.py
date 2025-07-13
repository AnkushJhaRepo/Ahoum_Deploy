#!/usr/bin/env python3
import sqlite3

DB_PATH = "instance/app.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check facilitator_id for session 24
target_session_id = 24
cursor.execute("SELECT id, facilitator_id FROM sessions WHERE id = ?", (target_session_id,))
session = cursor.fetchone()
print(f"Session {target_session_id}: facilitator_id = {session[1] if session else 'NOT FOUND'}")

# Print all facilitators
cursor.execute("SELECT id, name, email FROM users WHERE role = 'facilitator'")
print("\nAll facilitators:")
for row in cursor.fetchall():
    print(row)

conn.close() 