import sqlite3
from app import startConnection

connection = startConnection("database.db")
cur = connection.cursor()

req = "DELETE FROM movies WHERE id = 24 OR id = 25"
cur.execute(req)
connection.commit()