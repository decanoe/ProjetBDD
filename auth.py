from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")
@auth.route('/loginMethod', methods=['POST'])
def loginMethod():
    login = request.form['login']
    password = request.form['password']
    print(login, password)
    return render_template("profile.html")

@auth.route('/signup')
def signup():
    return render_template("signup.html")

@auth.route('/logout')
def logout():
    return "logout"
