import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Simple examples + constraints for all problems
c.execute("UPDATE problems SET examples='Input: 2,3\nOutput: 5', constraints='1 ≤ numbers ≤ 10^9' WHERE title='Sum of Two Numbers'")
c.execute("UPDATE problems SET examples='Input: 4\nOutput: Even', constraints='0 ≤ n ≤ 10^9' WHERE title='Check Even or Odd'")

# Add more later...
conn.commit()
conn.close()

print("Examples & Constraints added!")