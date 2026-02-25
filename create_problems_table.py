import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    stage INTEGER NOT NULL
)
""")

# Optional: insert sample problems
c.execute("""
INSERT INTO problems (title, description, stage)
VALUES
('Sample Problem 1', 'Write code to print Hello World', 1),
('Sample Problem 2', 'Find sum of two numbers', 1)
""")

conn.commit()
conn.close()

print("Problems table created successfully!")