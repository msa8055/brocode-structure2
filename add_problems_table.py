import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    stage INTEGER,
    difficulty TEXT
)
""")

conn.commit()
conn.close()

print("Problems table added!")