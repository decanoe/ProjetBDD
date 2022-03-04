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

#connection = startConnection("database.db")
#cur = connection.cursor()

#cur.execute('DROP TABLE comments')
#cur.execute('CREATE TABLE users ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "login" TEXT UNIQUE NOT NULL, "password" TEXT NOT NULL, "email" TEXT UNIQUE NOT NULL, "age" INTEGER NOT NULL)')
#cur.execute('CREATE TABLE movies ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "title" TEXT NOT NULL, "realisator" TEXT NOT NULL, "date" DATE, "duration" INTEGER, "image_path" TEXT NOT NULL, "genres" TEXT NOT NULL, "resum" TEXT NOT NULL, "resum_author" INTGER NOT NULL, FOREIGN KEY("resum_author") REFERENCES "users"("id"))')
#cur.execute('CREATE TABLE comments ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "movie" INTEGER, "user" INTEGER, "content" TEXT NOT NULL, "date" DATE, FOREIGN KEY("user") REFERENCES "users"("id"), FOREIGN KEY("movie") REFERENCES "movies"("id"))')
#connection.commit()
'''
cur.execute('SELECT * FROM users')

for row in cur.fetchall():
	print(row)'''

if __name__ == "__main__":
    create_app().run(debug=True)