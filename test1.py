from sqlite3 import Cursor
from matplotlib.pyplot import connect
from app import startConnection

connection = startConnection("database.db")
cursor = connection.cursor()

for i in range(5):
    cursor.execute("INSERT INTO posts (author,title,content) VALUES ('perso"+str(i)+"', 'title"+str(i)+"', 'content"+str(i)+"');")

connection.commit()
connection.close()