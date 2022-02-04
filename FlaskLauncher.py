import sqlite3
from sqlite3 import Error
from tracemalloc import start
from flask import *
app = Flask(__name__)

@app.route('/')
def home():
	print("launched")
	return render_template("index.html")

@app.route('/Forum')
def forum():
	return render_template("forum.html")
	
if __name__ == "__main__":
	app.run()


# tests

def startConnection(path):
    connect = None
    try:
        connect = sqlite3.connect(path)
    except Error as e:
        print(e)

    return connect

connection = startConnection("database.db")

cur = connection.cursor()
#cur.execute('CREATE TABLE users ("pseudo" TEXT NOT NULL, "password" TEXT NOT NULL, "email" TEXT NOT NULL, "age" INTEGER NOT NULL, PRIMARY KEY("email"))')
#cur.execute('DROP TABLE users')
'''
cur.execute('SELECT * FROM users')

for row in cur.fetchall():
	print(row)'''