import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS problems")

conn.commit()
conn.close()

print("✔ problems table deleted!")