# <div ID="success"></div>: Daniel Yentin, Ivan Yeung
# SoftDev
# Nov 2022

import sqlite3

DB_FILE = "database.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()


from flask import *
# from flask import Flask             #facilitate flask webserving
# from flask import render_template   #facilitate jinja templating
# from flask import request           #facilitate form submission
# from flask import session           #facilitate form submission
# from flask import redirect           #facilitate form submission
# from flask import url_for

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
    form_username = request.form["username"]
    form_password = request.form["password"]

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute(f"SELECT * FROM users WHERE username = '{form_username}'")
    users = c.fetchall()

    if len(users) == 1:
        user = users[0]
        db_username = user[0]
        db_password = user[1]

        if (form_username == db_username):
            print("***DIAG: username matches ***")
            #checks if input for the password form matches with hardcoded password

            if (form_password == db_password):
                print("***DIAG: password matches ***")
                #when both coditions are met, password is stored in the cookie and the home page is rendered
                session["username"] = form_username
                return redirect("/home", 307)

            print("***DIAG: password did not match ***")
            return redirect("/login", 307)

        print("***DIAG: username did not match ***")
        return redirect("/login", 307)

    elif len(users) == 0:
        print("***DIAG: account does not exist ***")
        return redirect("/login", 307)

    else:
        return "YOU ARE A FAILURE AT CODING, GET A NEW JOB"

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route("/register/auth", methods=['GET', 'POST'])
def register_auth():
    username = request.form["username"]
    password = request.form["password"]

    if " " in username:
        print("***DIAG: username invalid, contains space***")
        return redirect("/register", 307)

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #checks if inputted username exists
    c.execute(f"SELECT username FROM users WHERE username = '{username}'")
    usernames = c.fetchall()

    if len(usernames) == 0:
        print("***DIAG: username was available***")
        c.execute(f"INSERT INTO users(username, password) VALUES('{username}', '{password}')")

        c.execute(f"CREATE TABLE {username}(stories TEXT)")

        db.commit()
        return redirect("/login", 307)

    print("***DIAG: username was not available***")
    return redirect("/register", 307)

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

@app.route("/create", methods=['GET', 'POST'])
def create():
    return render_template('create.html')

@app.route("/publish", methods=['GET', 'POST'])
def publish():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    title = request.form["title"]
    # if (title already exists dont do anything):
    #     print("***DIAG: title was not available***")

    body = request.form["body"]
    if (len(body) == 0):
        print("***DIAG: body cannot be empty***")
    if (len(body) > 200):
        print("***DIAG: body cannot be greater than 200 characters***")

    publisher = session["username"]

    # store story in stories table
    c.execute(f"INSERT INTO TABLE stories(title, body, publisher) VALUES({title}, {body}, {publisher})")
    
    # store story history in story table
    c.execute(f"CREATE TABLE {title}(contributors TEXT, contributions TEXT)")
    c.execute(f"INSERT INTO {title}({publisher}, {body})")

    db.commit()
    return redirect("/home", 307)

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #table storing usernames and passwords
    c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
    #table storing info on stories
    c.execute("CREATE TABLE IF NOT EXISTS stories(title TEXT, publisher TEXT, body TEXT)")

    db.commit()

    app.debug = True
    app.run()

    db.close()

