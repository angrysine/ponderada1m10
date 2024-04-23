import sqlite3
con = sqlite3.connect("sqlite.db")
cur = con.cursor()

cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT, password TEXT)")
cur.execute("CREATE TABLE tasks (title TEXT, content TEXT, userId INTEGER)")
con.commit()
con.close()