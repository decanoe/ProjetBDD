from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/profile')
def profile():
    return render_template("profile.html")

@main.route('/forum')
def forum():
    from auth import connectedAs as user
    print(user)
    return render_template("forum.html")