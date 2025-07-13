#!/usr/bin/env python3
"""
Ensure facilitator user has correct role
"""

import sqlite3

DB_PATH = "instance/app.db"

def fix_role():
    email = "facilitator@test.com"
    role = "facilitator"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
    conn.commit()
    cursor.execute("SELECT id, name, email, role FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    print(f"User: {user}")
    conn.close()

if __name__ == "__main__":
    fix_role() 