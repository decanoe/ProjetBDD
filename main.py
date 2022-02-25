from flask import Blueprint, render_template
from app import startConnection
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/profile')
def profile():
    from auth import connectedAs as user
    print(user)
    return render_template("profile.html")

@main.route('/forum')
def forum():
    return render_template("forum.html")

@main.route('/resetData', methods=['POST'])
def resetData():
    connection = startConnection("database.db")
    cur = connection.cursor()
    cur.execute("DELETE FROM users")
    connection.commit()
    connection.close()
    return render_template("index.html", message = "La table users a été reset")