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
  return hashlib.sha256(pw).hexdigest()

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
  if 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']
    confirm = request.form['confirm_password']    
    if username and password and confirm:
      if not db.isRegistered(username):
        if password == confirm:
          db.addUser(username, hash(password))
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

@app.route('/home/')
def home():
  return render_template('home.html')

if __name__ == '__main__':
  app.debug = True
  app.run()