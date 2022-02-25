import sqlite3
from app import startConnection
connection = startConnection("database.db")
cur = connection.cursor()
req = "INSERT INTO users (login,password,email,age) VALUES ('erwan2511','test','erwan.legrand@gmail.com',17)"
cur.execute(req)
req = "INSERT INTO users (login,password,email,age) VALUES ('totoro49','a','@rnaque.i',16)"
cur.execute(req)
cur.execute('select login from users')
list_login = cur.fetchone()
print(list_login)
connection.commit()
connection.close()