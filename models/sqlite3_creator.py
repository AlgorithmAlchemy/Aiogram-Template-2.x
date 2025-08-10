import sqlite3

# b_option = top secret auto back-up
db = sqlite3.connect('users.sqlite')
connect = db.cursor()

connect.execute('''CREATE TABLE IF NOT EXISTS invoice (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT,
  message_id  TEXT,
  status TEXT DEFAULT 0
)''')
