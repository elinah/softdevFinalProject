import sqlite3

c = None
db = None

def createDB():
  global c
  c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER, username TEXT, password TEXT, name TEXT, grade INTEGER, member TEXT, admin TEXT);')
  c.execute('CREATE TABLE IF NOT EXISTS clubs (club_id INTEGER, club_name TEXT, club_members TEXT, club_admins TEXT);')

def getMemName(id):
  initializeDB()
  c.execute('SELECT name FROM users WHERE (user_id = ?);',[id])
  out = c.fetchall()
  closeDB()
  return out

def getMemGrade(id):
  initializeDB()
  c.execute('SELECT grade FROM users WHERE (user_id = ?);',[id])
  out = c.fetchall()
  closeDB()
  return out

def getMemMembers(id):
  initializeDB()
  c.execute('SELECT member FROM users WHERE (user_id = ?);',[id])
  out = c.fetchall()
  closeDB()
  return out

def getMemAdmins(id):
  initializeDB()
  c.execute('SELECT admin FROM users WHERE (user_id = ?);',[id])
  out = c.fetchall()
  closeDB()
  return out

def getClubName(id):
  initializeDB()
  c.execute('SELECT club_name FROM clubs WHERE (club_id = ?);',[id])
  out = c.fetchall()
  closeDB()
  return out

def getClubMembers(id):
  initializeDB()
  c.execute('SELECT club_members FROM clubs WHERE (club_id = ?);',[id])
  out = c.fetchall()
  closeDB()
  return out

def getClubAdmins(id):
  initializeDB()
  c.execute('SELECT club_admins FROM clubs WHERE (club_id = ?);',[id])
  out = c.fetchall()
  closeDB()
  return out

def addClub(name, members, admins):
  initializeDB()
  c.execute('INSERT INTO clubs (club_name, club_members, club_admins) VALUES (?,?,?);',(name, members, admins))
  closeDB()

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
