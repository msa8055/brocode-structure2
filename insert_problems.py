import sqlite3

problems = [
    # Stage 1
    (1, "Variables & Input", "Easy", 10),
    (1, "Data Types", "Easy", 10),
    (1, "Basic Operators", "Easy", 10),

    # Stage 2
    (2, "If Conditions", "Easy", 15),
    (2, "Nested If", "Easy", 15),
    (2, "Logical Operators", "Easy", 15),

    # Stage 3
    (3, "For Loops", "Medium", 20),
    (3, "While Loops", "Medium", 20),
    (3, "Loop Patterns", "Medium", 25),

    # Stage 4
    (4, "Functions Basics", "Medium", 25),
    (4, "Arguments & Return", "Medium", 25),
    (4, "Function Problems", "Medium", 30),

    # Stage 5
    (5, "Lists", "Medium", 25),
    (5, "Tuples", "Medium", 25),
    (5, "List Operations", "Medium", 30),

    # Stage 6
    (6, "Dictionaries", "Hard", 40),
    (6, "Dictionary Problems", "Hard", 45),
    (6, "Sets & Maps", "Hard", 40),

    # Stage 7
    (7, "Basic Algorithms", "Hard", 50),
    (7, "Searching", "Hard", 50),
    (7, "Sorting", "Hard", 60),

    # Stage 8
    (8, "Strings", "Medium", 20),
    (8, "String Functions", "Medium", 25),
    (8, "String Problems", "Hard", 30),

    # Stage 9
    (9, "File Handling Basics", "Medium", 25),
    (9, "Reading & Writing", "Medium", 30),
    (9, "File Problems", "Hard", 40),

    # Stage 10
    (10, "OOP Basics", "Hard", 40),
    (10, "Classes & Objects", "Hard", 45),
    (10, "OOP Problems", "Hard", 50),
]

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.executemany("""
    INSERT INTO problems (stage, title, difficulty, xp)
    VALUES (?, ?, ?, ?)
""", problems)

conn.commit()
conn.close()
print("✔ All problems inserted successfully!")