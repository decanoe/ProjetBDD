import sqlite3
from app import startConnection

connection = startConnection("database.db")
cur = connection.cursor()

req = "UPDATE users SET email = 'erwan.legrand49@gmail.com' WHERE id = 1"
cur.execute(req)
connection.commit()