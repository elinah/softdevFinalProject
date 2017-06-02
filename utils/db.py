from itertools import chain
import sqlite3, json

c = None
db = None

#Created database schema
def createDB():
  global c
  # attendance: {member:days,member:days}
  c.execute('CREATE TABLE IF NOT EXISTS clubs (club_id INTEGER PRIMARY KEY NOT NULL, club_name TEXT, club_members TEXT, club_admins TEXT, description TEXT, announcements TEXT, attendance TEXT);')
  c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY NOT NULL, username TEXT NOT NULL, password TEXT, name TEXT, grade INTEGER, member TEXT, admin TEXT, attendance TEXT);')

#**********************************************                                                                                                                                                             
# Initialize, close DB                                                                                                                                                                                      
#**********************************************                                                                                                                                                             

def initializeDB():
  global c, db
  file = '../data/data.db'
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

def getClubDesc(name):
  initializeDB()
  c.execute('SELECT description FROM clubs WHERE (club_name = ?);',(name,))
  out = c.fetchall()
  closeDB()
  return out

# Returns club members + attendance - WORKS
def getClubMembers(name):
  initializeDB()
  c.execute('SELECT club_members FROM clubs WHERE (club_name = ?);',[name])
  allMembers = c.fetchall()
  allMembers = [a for a in allMembers[0]]
  allKeys = json.loads(allMembers[0].replace("'",'"')).keys()
  allValues = json.loads(allMembers[0].replace("'",'"')).values()
  lista = []
  for a in range(len(allKeys)):
    lista.append(str(allKeys[a])+" : "+str(allValues[a]))
  closeDB()
  return lista

#print(getClubMembers("Gam"))

def getClubAdmins(name):
  initializeDB()
  c.execute('SELECT club_admins FROM clubs WHERE (club_name = ?);',[name])
  out = c.fetchall()
  closeDB()
  return out[0]

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

#Changes password of user
def changePass(newPass, username):
  initializeDB()
  c.execute('UPDATE users SET password = ? WHERE (username = ?);',(newPass,username))
  closeDB()

#Changes name of user
def changeName(newName, username):
  initializeDB()
  c.execute('UPDATE users SET name = ? WHERE (username = ?);',(newName,username))
  closeDB()

#Changes grade of user
def changeGrade(newGrade, username):
  initializeDB()
  c.execute('UPDATE users SET grade = ? WHERE (username = ?);',(newGrade,username))
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

# Adds 1 to attendance for a member - WORKS
def addAttendance(name, username):
  initializeDB()
  c.execute('SELECT club_members FROM clubs WHERE (club_name = ?);',(name,))
  allMembers = c.fetchall()
  print(allMembers[0][0])
  allMembers = json.loads(allMembers[0][0].replace("'",'"'))
  allMembers[username] += 1
  allMembers = str(allMembers)
  print(allMembers)
  c.execute('UPDATE clubs SET club_members = ? WHERE (club_name = ?);',(allMembers, name))
  closeDB()

#addAttendance('Gam','gerry')

# Adds member to club - WORKS (for simple case)
def addUserToClub(name, username):
  initializeDB()
  c.execute('SELECT club_members FROM clubs WHERE (club_name = ?);',(name,))
  allMembers = c.fetchall()
  allMembers = json.loads(allMembers[0][0].replace("'",'"'))
  allMembers[username] = 0
  allMembers = str(allMembers)
  c.execute('UPDATE clubs SET club_members = ? WHERE (club_name = ?);',(allMembers, name))
  closeDB()

#addUserToClub('Gam','gerry')

#Adds club, adds club to admin+member list for founding user - WORKS
def addNewClub(name, username,description):
  initializeDB()
  c.execute('SELECT club_name from clubs;')
  all_clubs = c.fetchall()
  all_clubs = [a[0] for a in all_clubs]
  memberFormat = "{"+username+":0}"
  if str(name) not in all_clubs:
    c.execute('INSERT INTO clubs (club_name, club_members, club_admins, description) VALUES (?,?,?,?);', (name,memberFormat,username,description))
  c.execute('SELECT member from users WHERE (username = ?);',(username,))
  member_clubs = c.fetchall()
  if(member_clubs):
    member_clubs = list(member_clubs[0])
    print(member_clubs)
    if (member_clubs[0] != None):
      member_clubs = member_clubs[0].split(",")
    else:
      member_clubs = []
  if str(name) not in member_clubs:
    member_clubs.append(name)
  member_clubs = ','.join(member_clubs)
  c.execute('UPDATE users SET member = ? WHERE (username = ?);',(member_clubs, username))
  c.execute('SELECT admin from users WHERE (username = ?);',(username,))
  admin_clubs = c.fetchall()
  if(admin_clubs):
    admin_clubs = list(admin_clubs[0])
    if (admin_clubs[0] != None):
      admin_clubs = admin_clubs[0].split(",")
    else:
      admin_clubs = []
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
      print(i)
      if (i[0] != None):
        i = list(i)[0].split(",")
        if str(name) in i:
          i.remove(str(name))
      else:
        i = []
      i = ",".join(str(j) for j in i)
      c.execute('UPDATE users SET member = ? WHERE (user_id = ?);',(i,count))
      count += 1
  c.execute('SELECT admin from users;')
  all_members = c.fetchall()
  count = 1
  if (all_members):
    for i in all_members:
      if(i[0] != None):
        i = list(i)[0].split(",")
        if str(name) in i:
          i.remove(str(name))
      else:
        i = []
      i = ",".join(str(j) for j in i)
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


# Adds announcements - WORKS
def addAnnouncements(name, announcement):
  initializeDB()
  c.execute('SELECT announcements FROM clubs WHERE (club_name = ?);',(name,))
  allAnnounce = c.fetchall()
  if(allAnnounce[0][0] != None):
    allAnnounce = [a[0] for a in allAnnounce]
  if(allAnnounce[0]!='' and allAnnounce[0] !=None):
    allAnnounce = allAnnounce[0]+","+announcement
  else:
    allAnnounce = announcement
  c.execute('UPDATE clubs SET announcements = ? WHERE (club_name = ?);',(allAnnounce,name))
  closeDB()

#addAnnouncements("Garl", "We are meeting in the bigger library!")

# Checks if user is admin - WORKS
def checkAdmin(name, username):
  initializeDB()
  c.execute('SELECT club_admins from clubs WHERE (club_name = ?);',(name,))
  allAdmins = c.fetchall()
  allAdmins = allAdmins[0][0]
  closeDB()
  return username in allAdmins

#checkAdmin('Book Club','sharon')

# To Do: changeToAdmin, removeAdmin, changeGrade, changeName, changePassword, incorporate emails
# 

