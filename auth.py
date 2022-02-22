from flask import Blueprint, render_template, request
from numpy import require

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/loginMethod', methods=['POST'])
def loginMethod():
    login = request.form['login']
    password = request.form['password']
    print(login, password)
    text = "Connecté en tant que %s" % (login)
    return render_template("profile.html", message = text)

@auth.route('/signup', methods=['POST'])
def signupMethod():
    login = request.form['login']
    password = request.form['password']
    email = request.form['email']
    age = request.form['age']
    print(login, password, email, age)
    text = "Connecté en tant que %s" % (login)
    return render_template("profile.html", message = text)

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/logout')
def logout():
    return "logout"
