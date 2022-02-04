import sqlite3
from sqlite3 import Error
from tracemalloc import start
from django.shortcuts import render
from flask import *
app = Flask(__name__)

@app.route('/')
def home():
	print("launched")
	return render_template("index.html")

if __name__ == "__main__":
	app.run()

# tests

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

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