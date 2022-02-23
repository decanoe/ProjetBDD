import sqlite3
from sqlite3 import Error
from flask import Flask

def create_app():
    app = Flask(__name__)

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def startConnection(path):
    connect = None
    try:
        connect = sqlite3.connect(path)
    except Error as e:
        print(e)

    return connect

connection = startConnection("database.db")

"""
cur.execute('CREATE TABLE users ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "login" TEXT NOT NULL, "password" TEXT NOT NULL, "email" TEXT NOT NULL, "age" INTEGER NOT NULL)')
cur.execute('CREATE TABLE posts ("id_post" INTEGER PRIMARY KEY AUTOINCREMENT, "autor" INTEGER, "title" TEXT NOT NULL, "content" TEXT NOT NULL, FOREIGN KEY("autor") REFERENCES "users"("id"))')
cur.execute('CREATE TABLE comments ("id_comment" INTEGER PRIMARY KEY AUTOINCREMENT, "post" INTEGER, "user" INTEGER, "content" TEXT NOT NULL, FOREIGN KEY("user") REFERENCES "users"("id"), FOREIGN KEY("post") REFERENCES "posts"("id_post"))')
"""
'''
cur.execute('SELECT * FROM users')

for row in cur.fetchall():
	print(row)'''

if __name__ == "__main__":
    create_app().run(debug=True)