import sqlite3
from app import startConnection

connection = startConnection("database.db")
cur = connection.cursor()

req = "DELETE FROM movies WHERE id = 27 OR id = 28"
cur.execute(req)
connection.commit()