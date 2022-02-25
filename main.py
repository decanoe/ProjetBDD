from flask import Blueprint, render_template
from app import startConnection
<<<<<<< HEAD
=======
from pythonClass.post import Post

>>>>>>> b44f00aa55a977d059c3d74a8c3c2128cc881c24
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

@main.route('/resetData', methods=['POST'])
def resetData():
    connection = startConnection("database.db")
    cur = connection.cursor()
    cur.execute("DELETE FROM users")
    connection.commit()
    connection.close()
    return render_template("index.html", message = "La table users a été reset")
