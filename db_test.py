import sqlite3

database = sqlite3.connect("security.db")

rows = database.execute("SELECT * FROM events").fetchall()

for row in rows:
    print(row)

database.close()