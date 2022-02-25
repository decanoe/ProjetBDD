from flask import Blueprint, render_template
from app import startConnection
from pythonClass.post import Post

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
    connection = startConnection("database.db")
    cursor = connection.cursor()

    list_post = []
    for post in cursor.execute("SELECT * FROM posts").fetchall():
        list_post.append(Post(post[0], post[1], post[2]))
    
    return render_template("forum.html", list_post = list_post)