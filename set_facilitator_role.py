import sqlite3

DB_PATH = 'instance/app.db'
EMAIL = 'facilitator_gvt2zb@test.com'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("UPDATE users SET role='facilitator' WHERE email=?", (EMAIL,))
conn.commit()

cursor.execute("SELECT id, name, email, role FROM users WHERE email=?", (EMAIL,))
user = cursor.fetchone()

if user:
    print(f"User updated: id={user[0]}, name={user[1]}, email={user[2]}, role={user[3]}")
else:
    print("User not found.")

conn.close() 