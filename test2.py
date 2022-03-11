import sqlite3
from app import startConnection
from passlib.hash import sha256_crypt

connection = startConnection("database.db")
cur = connection.cursor()

list_mdp = ['3r1.LgRd','a','123aze']

for mdp in list_mdp:
    hash = sha256_crypt.encrypt(mdp)
    req = "UPDATE users SET password= '" + hash + "'WHERE password ='" + mdp + "';"
    cur.execute(req)
    connection.commit()
