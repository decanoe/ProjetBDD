import sqlite3
from app import startConnection

connection = startConnection("database.db")
cur = connection.cursor()

req = "SELECT genres FROM movies WHERE id>10 AND id<14"
result = cur.execute(req).fetchall()

list_genres = []
for genres in result:
    list_genres.append("Animation, " + genres[0])

req = "UPDATE movies SET genres = '"+ list_genres[2] + "' WHERE id = " +str(13)
print(req)
cur.execute(req)
connection.commit()