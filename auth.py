from glob import glob
from tracemalloc import stop
from flask import Blueprint, render_template, request
import sqlite3
from app import startConnection

auth = Blueprint('auth', __name__)

connectedAs = None

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/loginMethod', methods=['POST'])
def loginMethod():
    login = request.form['login']
    password = request.form['password']

    connection = startConnection("database.db")
    cur = connection.cursor()
    cur.execute('SELECT * FROM users WHERE login = "' + login + '" AND password = "' + password + '";')
    exist = (cur.fetchone() == None)
    connection.close()
    if not(exist):
        global connectedAs
        connectedAs = login
        return render_template("profile.html", message = "Connecté en tant que %s" % (login))
    else:
        return render_template("login.html", message = "Identifiant ou mot de passe incorrect")


@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/signupMethod', methods=['POST'])
def signupMethod():
    login = request.form['login']
    password = request.form['password']
    email = request.form['email']
    age = request.form['age']

    connection = startConnection("database.db")
    cur = connection.cursor()

    #Test for empty fields
    if login == "" or password == "" or email == "" or age == "":
        text = "Veuillez remplir tous les formulaires afin de créer votre compte"
        return render_template("signup.html", message = text)
    
    # --- Login Tests ---
    elif len(login) > 30:
        text ="Votre login est trop long (max 30 caractères). "
        return render_template("signup.html", message = text)
    elif cur.execute('SELECT login FROM users WHERE login = "' + login + '";').fetchone() != None:
        text = "Ce pseudonyme est déjà utilisé"
        print('DEJA UTILISE')
        return render_template("signup.html", message = text)
    
    # --- password ---
    elif len(password) > 30:
        text ="Votre mot de passe est trop long (max 30 caractères). "
        return render_template("signup.html", message = text)
    
    # --- email ---
    elif cur.execute('SELECT email FROM users WHERE email = "' + email + '";').fetchone() != None:
        text = "Cette adresse email est déjà utilisée"
        return render_template("signup.html", message = text)
    
    else:
        cur.execute("INSERT INTO users (login,password,email,age) VALUES ('" + login + "','" + password + "','" + email + "'," + str(age) + ");")
        connection.commit()
        connection.close()
        text = "Votre compte à bien été créer. Vous êtes connecté en tant que %s" % (login)
        return render_template("profile.html", message = text)

@auth.route('/logout')
def logout():
    global connectedAs
    connectedAs = None
    return render_template("login.html")
