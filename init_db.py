import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage INTEGER NOT NULL,
    problem TEXT NOT NULL,
    answer TEXT NOT NULL
);
""")

print("Table created successfully.")
conn.commit()
conn.close()