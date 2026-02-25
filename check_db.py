import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

print("\nTABLE STRUCTURE:\n")
cur.execute("PRAGMA table_info(problems)")
print(cur.fetchall())

print("\nTABLE ROWS:\n")
cur.execute("SELECT id, title, description, stage, examples, constraints FROM problems")
rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()