import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE users ADD COLUMN profile_pic TEXT")
    print("Column 'profile_pic' added!")
except:
    print("Column already exists!")

conn.commit()
conn.close()