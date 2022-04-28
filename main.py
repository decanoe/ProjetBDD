from warnings import filters
from flask import Blueprint, render_template, redirect, request
from pkg_resources import resource_listdir
from app import startConnection
from pythonClass.movie import Movie
from pythonClass.comment import Comment
from pythonClass.user import User
from pythonClass.roundNote import roundNote, moyTuple
import datetime
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)

#page d'accueil
@main.route('/')
def index():
    from auth import connectedAs as user
    return render_template("index.html", connectedAs = user)

#page profile utilisateur
@main.route('/profile/<int:id_user>')
def profile(id_user):
    connection = startConnection("database.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = " + str(id_user) + ";")
    result = cur.fetchone()
    user = User(result[0], result[1], result[2], result[3], result[4])
    cur.execute("SELECT COUNT(*) FROM comments WHERE user = " + str(id_user) + ";")
    nComment = cur.fetchone()[0]
    from auth import connectedAs
    return render_template("profile.html", connectedAs = connectedAs, user = user, nComment = nComment)

#page forum
@main.route('/forum')
def forum():
    connection = startConnection("database.db")
    cursor = connection.cursor()
    list_movie = []
    for result in cursor.execute("SELECT movies.id, title, realisator, date, duration, image_path, genres, resum, login, users.id, creation_date FROM movies JOIN users ON users.id = movies.resum_author").fetchall():
        list_movie.append(Movie(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10]))
    reals = ["Tous"]
    for real in cursor.execute("SELECT DISTINCT realisator FROM movies").fetchall():
        reals.append(real[0])
    from auth import connectedAs as user
    return render_template("forum.html", list_movie = list_movie, connectedAs = user, reals = reals)

#fonction pour reset la table user (pas accessible depuis le site web)
@main.route('/resetData', methods=['POST'])
def resetData():
    connection = startConnection("database.db")
    cur = connection.cursor()
    cur.execute("DELETE FROM users")
    connection.commit()
    connection.close()

    from auth import connectedAs as user
    return render_template("index.html", message = "La table users a été reset", connectedAs = user)

#poster un commentaire
@main.route("/comment", methods=["POST"])
def comment():
    from auth import connectedAs as user
    connection = startConnection("database.db")
    cursor = connection.cursor()
    id_movie = request.form['id_movie']
    content = request.form['content'].replace("'","''").replace('\n','<br>')
    date = datetime.datetime.today().date()
    split_date = str(date).split('-')
    date = split_date[2]+'-'+split_date[1]+'-'+split_date[0]
    cursor.execute("INSERT INTO comments (movie,user,content,date) VALUES("+str(id_movie)+","+str(user.id)+",'"+content+"','" + str(date) + "')")
    connection.commit()
    connection.close()
    return redirect("/movie/"+str(id_movie))

#page avec les formulaires pour ajouter un film
@main.route('/postMovie')
def postMovie():
    from auth import connectedAs as user
    return render_template("postMovie.html", connectedAs = user)

#ajout du film à la base de donnée
@main.route("/postMovie", methods=["POST"])
def postMovieMethod():
    from auth import connectedAs as user
    connection = startConnection("database.db")
    cursor = connection.cursor()
    title = request.form['title'].replace("'","''")
    realisator = request.form['realisator'].replace("'","''")
    date = request.form['date']
    split_date = str(date).split('-')
    date = split_date[2]+'-'+split_date[1]+'-'+split_date[0]
    duration = request.form['duration']
    file = request.files['image']
    filename = secure_filename(file.filename)
    image_path = "/static/movies/"+filename
    file.save(os.path.join('static/movies', filename))
    genres = request.form['genres']
    resum = request.form['resum'].replace("'","''").replace('\n','<br>')
    creation_date = datetime.datetime.today().date()
    split_date = str(creation_date).split('-')
    creation_date = split_date[2]+'-'+split_date[1]+'-'+split_date[0]
    req = "INSERT INTO movies (title, realisator, date, duration, image_path, genres, resum, resum_author, creation_date) VALUES "
    req+= "('" + title + "','" + realisator + "','" + str(date) + "'," + str(duration) + ",'" + image_path + "','" + genres + "','" + resum + "'," + str(user.id) + ",'" + creation_date + "');"
    cursor.execute(req)
    connection.commit()
    req = "SELECT id FROM movies WHERE resum_author ="+str(user.id)+" AND title ='"+title+"' AND resum ='"+resum+"';"
    id_movie = cursor.execute(req).fetchone()[0]
    connection.close()
    return redirect("/movie/"+str(id_movie))

#page film
@main.route('/movie/<int:id_movie>')
def MoviePage(id_movie):
    connection = startConnection("database.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT movies.id, title, realisator, date, duration, image_path, genres, resum, login, users.id, creation_date  FROM movies JOIN users ON users.id = movies.resum_author WHERE movies.id="+str(id_movie)+";").fetchone()
    movie = Movie(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10])
    
    result = cursor.execute("SELECT movie, login, users.id, content, date FROM comments JOIN users ON users.id = comments.user WHERE movie="+str(id_movie)+";").fetchall()
    list_comment = []
    for comment in result:
        list_comment.append(Comment(comment[0],comment[1],comment[2],comment[3], comment[4]))
    list_comment.reverse()
    req = "SELECT note FROM notes WHERE id_film = " + str(movie.id)
    notes = cursor.execute(req).fetchall()
    if notes != []:
        moyenne = roundNote(moyTuple(notes))
    else:
        moyenne = None
    
    from auth import connectedAs as user
    return render_template("movie.html", movie = movie, list_comment = list_comment, connectedAs = user, moyenne = moyenne)

@main.route('/movie/<int:id_movie>/<int:note>')
def addNote(id_movie,note):
    note = max(min(note, 5), 0)
    from auth import connectedAs as user

    connection = startConnection("database.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT COUNT(*) FROM notes WHERE user = " + str(user.id) + " AND id_film = " + str(id_movie) + ";").fetchone()[0]
    if result == 0:
        cursor.execute("INSERT INTO notes (user,id_film,note) VALUES (" + str(user.id) + ", " + str(id_movie) + ", " + str(note) + ");")
    else:
        cursor.execute("UPDATE notes SET note =" + str(note) + " WHERE user = " + str(user.id) + " AND id_film = " + str(id_movie) + ";")
    
    connection.commit()
    connection.close()

    return redirect("/movie/"+str(id_movie))

@main.route('/forum/filtre', methods=["POST"])
def filtrer():
    reals = ["Tous"]
    connection = startConnection("database.db")
    cursor = connection.cursor()
    for real in cursor.execute("SELECT DISTINCT realisator FROM movies").fetchall():
        reals.append(real[0])
    index_real = int(request.form['tri-real'])
    if index_real == 0:
        return redirect("/forum")
    real = reals[index_real]
    req = "SELECT movies.id, title, realisator, date, duration, image_path, genres, resum, login, users.id, creation_date FROM movies JOIN users ON users.id = movies.resum_author WHERE realisator='"+real+"'"
    results = cursor.execute(req).fetchall()
    list_movie = []
    for result in results:
        list_movie.append(Movie(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10]))
    from auth import connectedAs as user
    return render_template("forum.html", list_movie = list_movie, connectedAs = user, reals = reals, filters = filters)