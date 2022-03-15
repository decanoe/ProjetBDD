import sqlite3
from sqlite3 import Error
from flask import Flask


#créer l'application web
def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'static/movies'

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

#fonction qui permet de se connecter une base de donnée
def startConnection(path):
    connect = None
    try:
        connect = sqlite3.connect(path)
    except Error as e:
        print(e)

    return connect


#juste au cas où :
"""
connection = startConnection("database.db")
cur = connection.cursor()

cur.execute('DROP TABLE comments')
cur.execute('CREATE TABLE users ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "login" TEXT UNIQUE NOT NULL, "password" TEXT NOT NULL, "email" TEXT UNIQUE NOT NULL, "age" INTEGER NOT NULL)')
cur.execute('CREATE TABLE movies ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "title" TEXT NOT NULL, "realisator" TEXT NOT NULL, "date" DATE, "duration" INTEGER, "image_path" TEXT NOT NULL, "genres" TEXT NOT NULL, "resum" TEXT NOT NULL, "resum_author" INTGER NOT NULL, FOREIGN KEY("resum_author") REFERENCES "users"("id"))')
cur.execute('CREATE TABLE comments ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "movie" INTEGER, "user" INTEGER, "content" TEXT NOT NULL, "date" DATE, FOREIGN KEY("user") REFERENCES "users"("id"), FOREIGN KEY("movie") REFERENCES "movies"("id"))')
cur.execute('CREATE TABLE notes ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "user" INTEGER, "id_film" INTEGER, "note" INTEGER, FOREIGN KEY("user") REFERENCES "users"("id"), FOREIGN KEY("id_film") REFERENCES "movies"("id"))')
connection.commit()
"""


#lancer l'application web

if __name__ == "__main__":
    create_app().run(debug=True)