from flask import Blueprint, render_template, request, flash
from app import startConnection
from pythonClass.user import User

auth = Blueprint('auth', __name__)

connectedAs = None

@auth.route('/login')
def login():
    return render_template("login.html", connectedAs = connectedAs)

@auth.route('/loginMethod', methods=['POST'])
def loginMethod():
    login = request.form['login']
    password = request.form['password']

    connection = startConnection("database.db")
    cur = connection.cursor()
    cur.execute('SELECT * FROM users WHERE login = "' + login + '" AND password = "' + password + '";')
    result = cur.fetchone()
    connection.close()
    if result != None:
        global connectedAs
        connectedAs = User(result[1], result[2], result[3], result[4])
        return render_template("profile.html", message = "Connecté en tant que %s" % (login), connectedAs = connectedAs)
    else:
        return render_template("login.html", message = "Identifiant ou mot de passe incorrect", connectedAs = connectedAs)


@auth.route('/signup')
def signup():
    return render_template("signup.html", connectedAs = connectedAs)

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
        return render_template("signup.html", message = text, connectedAs = connectedAs)
    
    # --- Login Tests ---
    elif len(login) > 30:
        text ="Votre login est trop long (max 30 caractères). "
        return render_template("signup.html", message = text, connectedAs = connectedAs)
    elif cur.execute('SELECT login FROM users WHERE login = "' + login + '";').fetchone() != None:
        text = "Ce pseudonyme est déjà utilisé"
        print('DEJA UTILISE')
        return render_template("signup.html", message = text, connectedAs = connectedAs)
    
    # --- password ---
    elif len(password) > 30:
        text ="Votre mot de passe est trop long (max 30 caractères). "
        return render_template("signup.html", message = text, connectedAs = connectedAs)
    
    # --- email ---
    elif cur.execute('SELECT email FROM users WHERE email = "' + email + '";').fetchone() != None:
        text = "Cette adresse email est déjà utilisée"
        return render_template("signup.html", message = text, connectedAs = connectedAs)
    
    else:
        cur.execute("INSERT INTO users (login,password,email,age) VALUES ('" + login + "','" + password + "','" + email + "'," + str(age) + ");")
        connection.commit()
        connection.close()
        return render_template("profile.html", connectedAs = connectedAs)

@auth.route('/logout')
def logout():
    global connectedAs
    connectedAs = None
    return render_template("login.html", connectedAs = None)
