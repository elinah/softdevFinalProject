from flask import Flask, render_template, request, session, redirect, url_for
from utils import db
import hashlib

app = Flask(__name__)

app.secret_key = 'key'

msg = ' '

def isLoggedIn():
  if 'username' in session:
    if db.isRegistered(session['username']):
      return True
    session.pop('username')
  return False

def hash(pw):
  return hashlib.sha256(pw.encode('utf-8')).hexdigest()

@app.route('/')
def default():
  if isLoggedIn():
    return redirect(url_for('home'))
  return redirect(url_for('auth'))

@app.route('/auth/')
def auth():
  if isLoggedIn():
    return redirect(url_for('default'))
  return render_template('auth.html', message = msg)

@app.route('/login/', methods = ['POST'])
def login():
  global msg
  if 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']
    if db.authUser(username, hash(password)):
      session['username'] = username
    else:
      msg = 'Incorrect username or password!'
  else:
    msg = 'Please fill out all fields!'
  return redirect(url_for('default'))

@app.route('/register/', methods = ['POST'])
def register():
  global msg
  if 'username' in request.form and 'password' in request.form and 'confirmPassword' in request.form and 'name' in request.form and 'grade' in request.form:
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirmPassword']
    name = request.form['name']
    grade = request.form['grade']
    if username and password and confirm and name and grade:
      if not db.isRegistered(username):
        if password == confirm:
          db.addUser(username, hash(password), name, grade)
          session['username'] = username
        else:
          msg = 'Passwords must match!'
      else:
        msg = 'Username already in use!'
    else:
      msg = 'Please fill out all fields!'
  else:
    msg = 'Please fill out all fields!'
  return redirect(url_for('default'))

@app.route("/logout/")
def logout():
  global msg
  if isLoggedIn():
    session.pop("username")
    msg = ' '
  return redirect(url_for("default"))

@app.route('/club/')
def club():
  return render_template('club.html')

@app.route('/add-clubs/')
def add_clubs():
  return render_template('add_club.html')

@app.route('/clubpage/<club>/', methods=["GET","POST"])
def clubpage(club):
  allMembers = db.getClubMembers(club)
  allAnn = db.getAnnouncements(club)
  isAdmin = db.checkAdmin(club,session['username'])
  isMember = db.checkMember(club,session['username'])
  present = db.getPresent(club,session['username']) 
  absent = db.getAbsent(club,session['username'])
  tdays = db.getTotalDays(club)
  return render_template('club.html', clubName=club, clubDesc=db.getClubDesc(club)[0][0], members=allMembers, announcements = allAnn, admin = isAdmin, present = present, absent=absent, totaldays = tdays, member = isMember)

@app.route('/add-new-club/', methods=["GET", "POST"])
def add_new_club():
  db.addNewClub(request.form['club'],session['username'],request.form['description'])
  return redirect(url_for('home'))

@app.route('/join/<clubName>/', methods=["GET","POST"])
def join(clubName):
  db.addUserToClub(clubName, session['username'])
  return redirect('/clubpage/'+clubName+'/')

@app.route('/inc-attendance/<clubName>/<username>/', methods=["GET","POST"])
def inc(clubName, username):
  username = username.replace(' ','').replace(':','')
  username = ''.join(i for i in username if not i.isdigit())
  db.addAttendance(clubName, username)
  return redirect('/clubpage/'+clubName+'/')

@app.route('/sub-attendance/<clubName>/<username>/', methods=["GET","POST"])
def sub(clubName, username):
  username = username.replace(' ','').replace(':','')
  username = ''.join(i for i in username if not i.isdigit())
  db.subAttendance(clubName, username)
  return redirect('/clubpage/'+clubName+'/')

@app.route('/inc-total/<clubName>/', methods=["GET","POST"])
def inctotal(clubName):
  db.addTotal(clubName)
  return redirect('/clubpage/'+clubName+'/')

@app.route('/sub-total/<clubName>/', methods=["GET","POST"])
def subtotal(clubName):
  db.subTotal(clubName)
  return redirect('/clubpage/'+clubName+'/')

@app.route('/announce/<clubName>/', methods=["GET","POST"])
def announce(clubName):
  db.addAnnouncements(clubName,request.form['announce'])
  return redirect('/clubpage/'+clubName+'/')

@app.route('/announcement/',methods=["POST"])
def announcement(clubName):
  text = request.form['text'];
  return json.dumps({'status':'OK','text':text});

@app.route('/home/')
def home():
  your_clubs = db.getMemMembers(session['username'])
  your_admin = db.getMemAdmins(session['username'])
  clubs = db.getAllClubs()
  allAnn = db.getAllAnn(session['username'])
  return render_template('home.html', your_clubs=your_clubs, clubs=clubs, your_admin=your_admin, ann = allAnn)

@app.route('/settings/')
def settings():
  return render_template('settings.html')

@app.route('/settings/changePass', methods=["POST"])
def changePass():
  msg1 = ' '
  if isLoggedIn():
    username = session['username']
    if 'currPass' in request.form and 'newPass' in request.form and 'confirmPass' in request.form:
      currPass = request.form['currPass']
      newPass = request.form['newPass']
      confirmPass = request.form['confirmPass']
      if currPass and newPass and confirmPass:
        if db.authUser(username, hash(currPass)):
          if newPass == confirmPass:
            db.changePass(username, hash(newPass))
            msg1 = "Successfully changed password!"
          else:
            msg1 = "Passwords must match!"
        else:
          msg1 = "Incorrect password!"
      else:
        msg1 = "Please fill out all fields!"
    else:
      msg1 = "Please fill out all fields!"
    return render_template('settings.html', message = msg1)
  else:
    return redirect(url_for('default'))
      
@app.route('/settings/changeName', methods=["POST"])
def changeName():
  msg2 = ' '
  if isLoggedIn():
    username = session['username']      
    if 'newName' in request.form:
      newName = request.form['newName']
      if newName:
        db.changeName(username, newName)
        msg2 = "Successfully changed name!"
      else:
        msg2 = "Please fill out all fields!"
    else:
        msg2 = "Please fill out all fields!"
    return render_template('settings.html', message = msg2)
  else:
    return redirect(url_for('default'))
      
@app.route('/settings/changeGrade', methods=["POST"])
def changeGrade():
  msg3 = ' '
  if isLoggedIn():
    username = session['username']
    if 'newGrade' in request.form:
      newGrade = request.form['newGrade']
      if newGrade:
        db.updateGrade(username, newGrade)
        msg3 = "Successfully changed grade!"
      else:
        msg3 = "Please fill out all fields!"
    else:
        msg3 = "Please fill out all fields!"
    return render_template('settings.html', message = msg3)
  else:
    return redirect(url_for('default'))

@app.route('/checkDes/', methods=["POST"])
def checkDes():
  pass

if __name__ == '__main__':
  app.debug = True
  app.run()
