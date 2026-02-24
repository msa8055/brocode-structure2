import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE users ADD COLUMN bio TEXT")
    print("Column 'bio' added!")
except:
    print("Column already exists.")

conn.commit()
conn.close()