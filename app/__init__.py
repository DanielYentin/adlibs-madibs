# <div ID="success"></div>: Daniel Yentin, Ivan Yeung
# SoftDev
# Nov 2022

import sqlite3

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()


from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import session           #facilitate form submission
from flask import redirect           #facilitate form submission
from flask import url_for

username = "test"
password = "1234"

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object
app.secret_key = b"\xdcG4g\xebL\x98m\xacX\x03\x13\xef\xfeF0#\x07P\x07JN\xf1P|'\x9ak\x1f\xe2\xf2?"

@app.route("/", methods=['GET', 'POST'])
def root():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    #checks if cookie has username and password stored
    if ('username' in session):
        print("***DIAG: user has already logged  ***")
        return redirect("/home", 307)
    else:
        #returns login page if cookie does not have that information
        return redirect("/login", 307)

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')
    
@app.route("/login/auth", methods=['GET', 'POST'])
def login_auth():
    #checks if input for the username form matches with hardcoded username
    if (request.form["username"] == username):
        print("***DIAG: username matches ***")
        #checks if input for the password form matches with hardcoded password
        if (request.form["password"] == password):
            print("***DIAG: password matches ***")
            #when both coditions are met, password is stored in the cookie and the home page is rendered
            session["username"] = request.form["username"]
            return redirect("/home", 307)
        else:
            print("***DIAG: password did not match ***")
            return redirect("/login", 307)
    else:
        print("***DIAG: username did not match ***")
        return redirect("/login", 307)

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')
    
@app.route("/register/auth", methods=['GET', 'POST'])
def register_auth():
    return

@app.route("/logout", methods=['GET', 'POST'])
# this function is called by the logout button when it is pressed on the home page
def logout():
    #cookie holding password is removed
    session.pop("username")
    print("***DIAG: password removed from cookie ***")
    return redirect("/login", 307)

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified

    c.execute("create table if not exists users(username text, password text)")
    c.execute("create table if not exists stories(title text, creator text, body text, latest_contribution text)")

    app.debug = True
    app.run()
    
    db.close()
