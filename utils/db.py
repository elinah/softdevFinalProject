import sqlite3

c = None
db = None

def createDB():
  global c
  c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER, username TEXT, password TEXT, name TEXT, grade INTEGER);')
  c.execute('CREATE TABLE IF NOT EXISTS clubs (club_id INTEGER, club_name TEXT);')

def initializeDB():
  global c, db
  file = 'data/data.db'
  db = sqlite3.connect(file)
  c = db.cursor()
  createDB()

def closeDB():
  global db
  db.commit()
  db.close()

def addUser(username, password):
  initializeDB()
  c.execute('INSERT INTO users (username, password) VALUES(?, ?);', (username, password))
  closeDB()

def isRegistered(username):
  initializeDB()
  c.execute('SELECT * FROM users WHERE (username = ?);', [username])
  out = c.fetchall()
  closeDB()
  return bool(out)

def authUser(username, password):
  initializeDB()
  c.execute('SELECT password FROM users WHERE (username = ?);', [username])
  out = c.fetchall()
  closeDB()
  if out:
    return out[0][0] == password
  else:
    return False