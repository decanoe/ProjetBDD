from hashlib import sha3_256
from flask import Blueprint, render_template, request, redirect
from app import startConnection
from pythonClass.user import User
from passlib.hash import sha256_crypt

auth = Blueprint('auth', __name__)

connectedAs = None

#page pour se connecter
@auth.route('/login')
def login():
    return render_template("login.html", connectedAs = connectedAs)

#vérification de l'identifiants et du mot de passe dans la base de donnée
@auth.route('/loginMethod', methods=['POST'])
def loginMethod():
    login = request.form['login']
    password =  request.form['password']

    connection = startConnection("database.db")
    cur = connection.cursor()
    cur.execute('SELECT * FROM users WHERE login = "' + login + '";')
    result = cur.fetchone()
    connection.close()
    if result != None and sha256_crypt.verify(password, result[2]):
        global connectedAs
        connectedAs = User(result[0], result[1], result[2], result[3], result[4])
        from main import profile
        return profile(connectedAs.id)
    else:
        return render_template("login.html", message = "Identifiant ou mot de passe incorrect", connectedAs = connectedAs)

#page pour créer son compte
@auth.route('/signup')
def signup():
    return render_template("signup.html", connectedAs = connectedAs)

#vérifications du remplissage des formulaires puis ajout des informations du nouveau compte dans la BDD
@auth.route('/signup', methods=['POST'])
def signupMethod():
    login = request.form['login'].replace("'","''")
    password = request.form['password']
    email = request.form['email'].replace("'","''")
    age = request.form['age']

    connection = startConnection("database.db")
    cur = connection.cursor()
    
    global connectedAs

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
    
    # --- âge ---
    elif int(age) <=0:
        text ="Votre âge me semble douteux !"
        return render_template("signup.html", message = text, connectedAs = connectedAs)
    
    # --- email ---
    elif cur.execute('SELECT email FROM users WHERE email = "' + email + '";').fetchone() != None:
        text = "Cette adresse email est déjà utilisée"
        return render_template("signup.html", message = text, connectedAs = connectedAs)
    
    else:
        cur.execute("INSERT INTO users (login,password,email,age) VALUES ('" + login + "','" + sha256_crypt.encrypt(password) + "','" + email + "'," + str(age) + ");")
        
        cur.execute('SELECT * FROM users WHERE login = "' + login + '";')
        result = cur.fetchone()
        connectedAs = User(result[0], result[1], result[2], result[3], result[4])

        connection.commit()
        connection.close()
        return redirect("/profile/" + str(connectedAs.id))

#se déconnecter
@auth.route('/logout')
def logout():
    global connectedAs
    connectedAs = None
    return render_template("login.html", connectedAs = None)
