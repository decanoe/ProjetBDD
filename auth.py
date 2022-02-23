from flask import Blueprint, render_template, request
import sqlite3
from app import startConnexion

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/loginMethod', methods=['POST'])
def loginMethod():
    login = request.form['login']
    password = request.form['password']
    text = "Connecté en tant que %s" % (login)
    return render_template("profile.html", message = text)

@auth.route('/signupMethod', methods=['POST'])
def signupMethod():
    login = request.form['login']
    password = request.form['password']
    email = request.form['email']
    age = request.form['age']
    text = ""
    connexion = startConnexion("database.db")
    cur = connexion.cursor()
    cur.execute('select login from users')
    list_login = cur.fetchone()
    tuple(list_login)
    cur.execute('select email from users')
    list_email = cur.fetchone()
    tuple(list_email)
    if len(login)==0 or len(password)==0 or len(email)==0 or len(age)==0:
        text = "Veuillez remplir tous les formulaires afin de créer votre compte"
        return render_template("signup.html", message = text)
    elif len(login)>30:
        text+="Votre login est trop long (max 30 caractères). "
        return render_template("signup.html", message = text)
    elif login in list_login:
        text += "Ce pseudonyme est déjà utilisé"
        return render_template("signup.html", message = text)
    elif len(password)>30:
        text+="Votre mot de passe est trop long (max 30 caractères). "
        return render_template("signup.html", message = text)
    elif len(password)<5:
        text+="Votre mot de passe doit contenir au moins 5 caractères. "
        return render_template("signup.html", message = text)
    elif "@" not in email or "." not in email:
        text+="Votre email doit être valide. "
        return render_template("signup.html", message = text)
    elif email in list_email:
        text += "Cette adresse email est déjà utilisée"
        return render_template("signup.html", message = text)
    elif not age.isnumeric():
        text += "Vous devez indiquez un âge valide. "
        return render_template("signup.html", message = text)
    else:
        text = "Votre compte à bien été créer. Vous êtes connecté en tant que %s" % (login)
        return render_template("profile.html", message = text)

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/logout')
def logout():
    return "logout"
