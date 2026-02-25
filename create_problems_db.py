import sqlite3

conn = sqlite3.connect("problems.db")
c = conn.cursor()

# Drop old table
c.execute("DROP TABLE IF EXISTS problems")

# Create properly structured table
c.execute("""
CREATE TABLE problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage INTEGER NOT NULL,
    title TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    xp INTEGER NOT NULL,
    description TEXT NOT NULL,
    examples TEXT NOT NULL,
    constraints TEXT NOT NULL
)
""")

sample_data = [
    (1, "Print Hello World", "Easy", 10,
     "Write a Python program that prints 'Hello, World!'",
     "Input: (none)\nOutput:\nHello, World!",
     "Use print() function only."
    ),
    (1, "Add Two Numbers", "Easy", 20,
     "Write a function that takes two integers and returns their sum.",
     "Input: 2 3\nOutput: 5",
     "1 ≤ a, b ≤ 1000"
    )
]

c.executemany("""
INSERT INTO problems (stage, title, difficulty, xp, description, examples, constraints)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", sample_data)

conn.commit()
conn.close()

print("problems.db recreated successfully!")