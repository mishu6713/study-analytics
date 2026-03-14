import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users 
          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
          username TEXT, 
          password TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS study_logs 
          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
          user_id INTEGER, 
          date TEXT, 
          subject TEXT, 
          minutes INTEGER)""")

conn.commit()
conn.close()

print("database created")