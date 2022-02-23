from flask import Blueprint, render_template, request
from app import startConnection

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/loginMethod', methods=['POST'])
def loginMethod():
    login = request.form['login']
    password = request.form['password']
    cur = startConnection("database.db").cursor()
    cur.execute('SELECT login, password FROM users')
    for row in cur.fetchall():
	    if row == (login, password):
                print(login, password)
                text = "Connecté en tant que %s" % (login)
                return render_template("profile.html", message = text)

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/logout')
def logout():
    return "logout"
