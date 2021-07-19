from flask import Flask, g, redirect, render_template, request, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'somesecretkeythatishouldonlyknow'

class User():

    def __init__(self,id,username,password):
        self.id = id
        self.username = username
        self.password = password
    
    def __repr__(self): # IF YOU PRINT OUT A USER YOU WILL GET IT IN THIS FORMAT
        return f'<User: {self.username}> '

users = []
users.append(User(id=1, username='Mohamed', password = '12345'))        

print (users)

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None) # drops session before request is made

        username = request.form['username']
        password = request.form['password'] 

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/register', methods=['POST','GET'])
def register():
   
    return render_template('register.html')

