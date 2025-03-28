import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
c.execute("CREATE TABLE IF NOT EXISTS events (event_id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, amount REAL, user_id INTEGER, t INTEGER, FOREIGN KEY(user_id) REFERENCES users(user_id))")

print('Database initialised')


conn.commit()
conn.close()
