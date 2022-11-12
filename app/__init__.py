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
# from flask import p_redirect           #facilitate form submission
# from flask import url_for

#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object
app.secret_key = b"\xdcG4g\xebL\x98m\xacX\x03\x13\xef\xfeF0#\x07P\x07JN\xf1P|'\x9ak\x1f\xe2\xf2?"

def sql():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    return db, c

def p_redirect(url: str):
    '''
    flask redirect using post (307)
    '''
    return redirect(url, 307)

@app.route("/", methods=['GET', 'POST'])
def root():
    print("\n\n\n")
    print("***DIAG: this Flask obj ***")
    print(app)
    #checks if cookie has username and password stored
    if ('username' in session):
        print("***DIAG: user has already logged  ***")
        return p_redirect("/home")
    else:
        #returns login page if cookie does not have that information
        return p_redirect("/login")

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/login/auth", methods=['GET', 'POST'])
def login_auth():
    form_username = request.form["username"]
    form_password = request.form["password"]

    db, c = sql()
    # db = sqlite3.connect(DB_FILE)
    # c = db.cursor()

    print(form_username)
    c.execute("SELECT * FROM users WHERE username = ?", (form_username,))
    users = c.fetchall()

    if len(users) == 1:
        user = users[0]
        db_username = user[1]
        db_password = user[2]

        if (form_username == db_username):
            print("***DIAG: username matches ***")
            #checks if input for the password form matches with hardcoded password

            if (form_password == db_password):
                print("***DIAG: password matches ***")
                #when both coditions are met, password is stored in the cookie and the home page is rendered
                session["username"] = form_username
                return p_redirect("/home")

            print("***DIAG: password did not match ***")
            return p_redirect("/login")

        print("***DIAG: username did not match ***")
        return p_redirect("/login")

    elif len(users) == 0:
        print("***DIAG: account does not exist ***")
        return p_redirect("/login")

    else:
        return "YOU ARE A FAILURE AT CODING, GET A NEW JOB"

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route("/register/auth", methods=['GET', 'POST'])
def register_auth():
    db, c = sql()

    c.execute("SELECT * FROM users")
    next_available_uid = len(c.fetchall())
    print(next_available_uid)

    username = request.form["username"]
    password = request.form["password"]

    #checks if inputted username exists
    c.execute(f"SELECT username FROM users WHERE username = ?", (username,))
    usernames = c.fetchall()

    if len(usernames) == 0:
        print("***DIAG: username was available***")
        c.execute("INSERT INTO users(uid, username, password) VALUES(?, ?, ?)", (next_available_uid, username, password))
        c.execute(f"CREATE TABLE uid_{next_available_uid}(stories TEXT)")
        db.commit()
        return p_redirect("/login")

    print("***DIAG: username was not available***")
    return p_redirect("/register")

@app.route("/logout", methods=['GET', 'POST'])
# this function is called by the logout button when it is pressed on the home page
def logout():
    #cookie holding password is removed
    session.pop("username")
    print("***DIAG: password removed from cookie ***")
    return p_redirect("/login")

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route("/create", methods=['GET', 'POST'])
def create():
    return render_template('create.html')

@app.route("/publish", methods=['GET', 'POST'])
def publish():
    db, c = sql()

    c.execute("SELECT * FROM stories")
    next_available_sid = len(c.fetchall())
    print(f"next_available_sid: {next_available_sid}") #sid = story id

    title = request.form["title"]
    # if (title already exists dont do anything):
    #     print("***DIAG: title was not available***")

    body = request.form["body"]
    if (len(body) == 0):
        print("***DIAG: body cannot be empty***")
    if (len(body) > 200):
        print("***DIAG: body cannot be greater than 200 characters***")

    publisher = session["username"]

    # store story in stories table'
    c.execute(f"INSERT INTO stories(title, body, publisher) VALUES(?, ?, ?)", (title, body, publisher))
    print("***DIAG: story inserted into database***")

    # store story history in story table
    c.execute(f"CREATE TABLE sid_{next_available_sid}(contributors TEXT, contributions TEXT)")
    c.execute(f"INSERT INTO sid_{next_available_sid}(contributors, contributions) VALUES(?, ?)", (publisher, body))
    print("***DIAG: story's history inserted into database***")

    db.commit()
    return p_redirect("/home")


if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    db, c = sql()

    #table storing usernames and passwords
    c.execute("CREATE TABLE IF NOT EXISTS users(uid INT, username TEXT, password TEXT)")
    #table storing info on stories
    c.execute("CREATE TABLE IF NOT EXISTS stories(title TEXT, body TEXT, publisher TEXT)")

    db.commit()

    app.debug = True
    app.run()

    db.close()
