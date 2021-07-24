from flask import Flask, g, redirect, render_template, request, session, url_for
import os
from flask_sqlalchemy import SQLAlchemy
import psycopg2

########## DB CONFIG ##########


app = Flask(__name__)
app.config['SECRET_KEY'] = 'somesecretkeythatishouldonlyknow'


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@localhost:5433/login"

db = SQLAlchemy(app)


########### MODELS #######
class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    confirm_password = db.Column(db.String, nullable=False)
    
    def __repr__(self): # IF YOU PRINT OUT A USER YOU WILL GET IT IN THIS FORMAT
        return f'<User: {self.name}> ' 

@app.before_first_request 
def create_tables():
    db.create_all() # FOR CREATING MODELS ON LIVE SERVERS 
    
    
@app.route('/')
def home():
    
    return render_template('login.html')    

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None) # drops session before request is made

        email = request.form['email']
        password = request.form['password'] 

        user = User.query.filter_by(email = email).first()
        if user is not None:
            if user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('profile'))
            

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    # if not g.user:
    #     return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/register', methods=['POST','GET'])
def register():
   
    return render_template('register.html')

@app.route('/users')
def users():
    all_users = User.query.all()

    return render_template('users.html',all_users=all_users)
