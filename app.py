from flask import Flask, render_template, flash, redirect, url_for, request, session, logging, g #from flask, we want to import flask and render_template
from data import Reviews #from data.py, import the Reviews function
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import sqlite3

app = Flask(__name__) #creates an instance of flask
app.secret_key = "secret"
app.database = "database.db"

#MySQL configuration
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'localhost'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'mysql'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #makes it save as a dictionary instead of a tuple
#init MYSQL
#mysql = MySQL(app)

Reviews = Reviews()

def connect_db():
    return sqlite3.connect(app.database)

@app.route('/') #points flask to the index so it can load files
def index():
    return render_template('index.html', reviews = Reviews) #literally just return a string


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)]) #they must input a name between 1 and 50 characters
    username = StringField('Username', [validators.Length(min=4, max=25)]) #they must input a username between 4 and 25 characters
    email = StringField('Email', [validators.Length(min=6, max=50)]) #they must input a username between 4 and 25 characters
    password = PasswordField ('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'The passwords need to match yo')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods = ['GET', 'POST']) #needs to accept posts to collect data from the form
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate(): #need to make sure the request is post, and that it matches the validation
            name = form.name.data #if the user is submitting, make the name variable equal the name they input
            email = form.email.data
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data)) #encrypts the password before it's submitted.

            #Creates the DictCursor
            g.db = connect_db()
            g.db.execute("INSERT INTO users(name, email, username, password) VALUES(?, ?, ?, ?)", (name, email, username, password))
            g.db.commit()
            g.db.close()

            flash('You are now registered and can log in', 'success')
            redirect(url_for('index'))

    return render_template('register.html', form=form) #if not a POST, it must be a get. Serve the form.

if __name__ == '__main__': #if the right application is being run...
    app.run(debug = True) #run it. debut means you don't have to reload the server for every change
