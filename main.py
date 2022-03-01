from flask import Blueprint, render_template
from app import startConnection
from pythonClass.post import Post

main = Blueprint('main', __name__)

@main.route('/')
def index():
    from auth import connectedAs as user
    return render_template("index.html", connectedAs = user)

@main.route('/profile')
def profile():
    from auth import connectedAs as user
    print(user)
    return render_template("profile.html", connectedAs = user)

@main.route('/forum')
def forum():
    connection = startConnection("database.db")
    cursor = connection.cursor()

    list_post = []
    for post in cursor.execute("SELECT author, title, content FROM posts").fetchall():
        list_post.append(Post(post[0], post[1], post[2]))
    
    from auth import connectedAs as user
    return render_template("forum.html", list_post = list_post, connectedAs = user)

@main.route('/resetData', methods=['POST'])
def resetData():
    connection = startConnection("database.db")
    cur = connection.cursor()
    cur.execute("DELETE FROM users")
    connection.commit()
    connection.close()

    from auth import connectedAs as user
    return render_template("index.html", message = "La table users a été reset", connectedAs = user)

@main.route('/post/<int:post_id>')
def show_post(post_id):
    
    return render_template("post.html", post = )
