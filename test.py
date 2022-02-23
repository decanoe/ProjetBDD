import sqlite3
from app import startConnexion
connexion = startConnexion("database.db")
cur = connexion.cursor()
req = "INSERT INTO users (login,password,email,age) VALUES ('erwan2511','test','erwan.legrand@gmail.com',17)"
cur.execute(req)
cur.execute('select login from users')
list_login = cur.fetchone()
print(list_login)