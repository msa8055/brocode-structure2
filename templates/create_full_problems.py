import sqlite3

conn = sqlite3.connect("database.db")
conn.execute("DROP TABLE IF EXISTS problems")

conn.execute("""
CREATE TABLE problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage INTEGER,
    title TEXT,
    difficulty TEXT,
    xp INTEGER,
    description TEXT,
    examples TEXT,
    constraints TEXT
)
""")

problems = [
    # ---------- STAGE 1 ----------
    (1, "Print Hello World", "Easy", 10,
     "Write a Python program that prints 'Hello, World!'",
     "Input: none\nOutput: Hello, World!",
     "Use print()"),
     
    (1, "Add Two Numbers", "Easy", 20,
     "Write a function that returns sum of two numbers.",
     "Input: 2 3\nOutput: 5",
     "1 ≤ a, b ≤ 1000"),

    # ---------- STAGE 2 ----------
    (2, "Check Even/Odd", "Easy", 20,
     "Determine if a number is even or odd.",
     "Input: 4\nOutput: Even",
     "Use % operator"),

    (2, "Find Maximum", "Easy", 20,
     "Return the largest of three numbers.",
     "Input: 2 5 1\nOutput: 5",
     "Use if/else"),

    # ---------- STAGE 3 ----------
    (3, "Reverse String", "Medium", 30,
     "Reverse a given string.",
     "Input: hello\nOutput: olleh",
     "Use slicing or loop"),

    (3, "Sum of Digits", "Medium", 30,
     "Find sum of digits of a number.",
     "Input: 123\nOutput: 6",
     "Use loop"),

    # ---------- STAGE 4 ----------
    (4, "Palindrome Check", "Medium", 40,
     "Check if a string is palindrome.",
     "Input: madam\nOutput: Yes",
     "Ignore case"),

    (4, "Count Vowels", "Medium", 40,
     "Count number of vowels in a string.",
     "Input: python\nOutput: 1",
     "Vowels: a e i o u"),

    # ---------- STAGE 5 ----------
    (5, "Fibonacci", "Hard", 50,
     "Return nth Fibonacci number.",
     "Input: 6\nOutput: 8",
     "Use recursion or loop"),

    (5, "Two Sum", "Hard", 60,
     "Find indices of two numbers that sum to target.",
     "Input: [2,7,11,15], target=9\nOutput: [0,1]",
     "Use hash map"),

    # ---------- STAGE 6 ----------
    (6, "Binary Search", "Pro", 70,
     "Implement binary search.",
     "Input: [1,2,3,4], target=3\nOutput: 2",
     "Use O(log n)"),

    (6, "Sort Colors", "Pro", 80,
     "Sort an array of 0, 1, 2.",
     "Input: [2,0,1]\nOutput: [0,1,2]",
     "Use Dutch National Flag algorithm"),

    # ---------- STAGE 7 ----------
    (7, "LRU Cache", "Elite", 120,
     "Implement LRU Cache.",
     "Input: operations\nOutput: values",
     "Use OrderedDict or custom DLL"),

    (7, "Word Ladder", "Elite", 150,
     "Find shortest transformation path.",
     "Input: hit → cog\nOutput: 5",
     "Use BFS")
]

conn.executemany("""
INSERT INTO problems (stage, title, difficulty, xp, description, examples, constraints)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", problems)

conn.commit()
conn.close()

print("ALL STAGES UPDATED SUCCESSFULLY!")