import sqlite3
from app import startConnection

connection = startConnection("database.db")
cur = connection.cursor()
reals = []
for real in cur.execute("SELECT DISTINCT realisator FROM movies").fetchall():
    reals.append(real[0])

print(reals)
