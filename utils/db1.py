from itertools import chain
import sqlite3

c = None
db = None

#Created database schema
def createDB():
  global c
  c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER, username TEXT, password TEXT, name TEXT, grade INTEGER, member TEXT, admin TEXT);')
  c.execute('CREATE TABLE IF NOT EXISTS clubs (club_id INTEGER, club_name TEXT, club_members TEXT, club_admins TEXT);')


#**********************************************
# Accessor Methods
#**********************************************

def getMemId(name):
  initializeDB()
  c.execute('SELECT user_id from users WHERE(username = ?);', (name))
  out = c.fetchall()
  closeDB()
  return out
  
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

def getMemMembers(name):
  initializeDB()
  c.execute('SELECT member FROM users WHERE (username = ?);',(name,))
  out = c.fetchall()
  closeDB()
  return out

def getMemAdmins(name):
  initializeDB()
  c.execute('SELECT admin FROM users WHERE (username = ?);',(name,))
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

def getAllClubs():
  initializeDB()
  c.execute('SELECT club_name FROM clubs;')
  out = c.fetchall()
  closeDB()
  return out

#**********************************************
# Updating Methods
#**********************************************

def updateGrade(username, newGrade):
  initializeDB()
  c.execute('UPDATE users SET grade = ? WHERE (username = ?);',(newGrade, username))
  closeDB()

#**********************************************
# Initialize, close DB
#**********************************************
  
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

def deleteUserFromClub(name, username):
  intializeDB()
  c.execute('SELECT club_members FROM clubs WHERE (club_name = ?);', (name))
  allMembers = c.fetchall()
  allMembers = allMembers.split(',').remove(username)
  allMembers = ','.join(allMembers)
  c.execute('UPDATE clubs SET (club_members = allMembers) WHERE (club_name = ?);', (name))
  deleteClubFromUser(name, username)
  closeDB()
  

#***********************************************
# Authentication Methods
#***********************************************
  
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

#Adds club, adds club to admin+member list for founding user - WORKS
def addNewClub(name, username):
  initializeDB()
  c.execute('SELECT club_name from clubs;')
  all_clubs = c.fetchall()
  all_clubs = [a[0] for a in all_clubs]
  if str(name) not in all_clubs:
    c.execute('INSERT INTO clubs (club_name, club_members, club_admins) VALUES (?,?,?);', (name,username,username))
  c.execute('SELECT member from users WHERE (username = ?);',(username,))
  member_clubs = c.fetchall()
  if(member_clubs):
    member_clubs = list(member_clubs[0])
    member_clubs = member_clubs[0].split(",")
  if str(name) not in member_clubs:
    member_clubs.append(name)
  member_clubs = ','.join(member_clubs)
  c.execute('UPDATE users SET member = ? WHERE (username = ?);',(member_clubs, username))
  c.execute('SELECT admin from users WHERE (username = ?);',(username,))
  admin_clubs = c.fetchall()
  if(admin_clubs):
    admin_clubs = list(admin_clubs[0])
    admin_clubs = admin_clubs[0].split(",")
  if str(name) not in admin_clubs:
    admin_clubs.append(name)
  admin_clubs = ','.join(admin_clubs)
  c.execute('UPDATE users SET admin = ? WHERE (username = ?);',(admin_clubs, username))
  closeDB()

#addNewClub("Snow Club","sharon")

#Deletes club - WORKS
def deleteClub(name):
  initializeDB()
  c.execute('DELETE FROM clubs WHERE (club_name = ?);',(name,))
  c.execute('SELECT member from users;')
  all_members = c.fetchall()
  count = 1
  if (all_members):
    for i in all_members:
      i = list(i)[0].split(",")
      if str(name) in i:
        i.remove(str(name))
      i = ",".join(str(j) for j in i)
      c.execute('UPDATE users SET member = ? WHERE (user_id = ?);',(i,count))
      count += 1
  c.execute('SELECT admin from users;')
  all_members = c.fetchall()
  count = 1
  if (all_members):
    for i in all_members:
      if(i[0] != None):
        print(i)
        i = list(i)[0].split(",")
        if str(name) in i:
          i.remove(str(name))
      else:
        i = []
      i = ",".join(str(j) for j in i)
      print(i)
      c.execute('UPDATE users SET admin = ? WHERE (user_id = ?);',(i,count))
      count += 1
  closeDB()

#deleteClub("Fo Club")

#Adds user
def addUser(name, password):
  initializeDB()
  c.execute('INSERT INTO users (username, password) VALUES (?,?);',(name, password))
  closeDB()

#Adds club to member list for user
def addClubToUser(name, username):
  initializeDB()
  members = getMemMembers(username)
  if name not in members:
    members = ','.join(members)
    members = members+','+name
    c.execute('UPDATE users SET (member = ?) WHERE (username = ?);',(members,username))
  closeDB()

#Adds club to admin list for user
def addAdminToUser(name, username):
  initializeDB()
  members = getMemAdmins(username)
  if name not in members:
    members = ','.join(members)
    members = members+','+name
    c.execute('UPDATE users SET (admin = ?) WHERE (username = ?);',(members,username))
  closeDB()
