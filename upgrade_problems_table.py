import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Add missing columns if not exist
try:
    c.execute("ALTER TABLE problems ADD COLUMN examples TEXT")
except:
    pass

try:
    c.execute("ALTER TABLE problems ADD COLUMN constraints TEXT")
except:
    pass

conn.commit()
conn.close()

print("Problems table upgraded successfully!")