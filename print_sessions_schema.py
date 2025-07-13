#!/usr/bin/env python3
import sqlite3

DB_PATH = "instance/app.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Schema for 'sessions' table:")
cursor.execute("PRAGMA table_info(sessions)")
for row in cursor.fetchall():
    print(row)

conn.close() 