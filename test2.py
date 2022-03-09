import sqlite3
from app import startConnection

connection = startConnection("database.db")
cur = connection.cursor()

req = "DELETE FROM comments WHERE user>2 AND user <> 14"
cur.execute(req)
connection.commit()