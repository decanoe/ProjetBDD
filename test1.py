"""from app import startConnection
import random

posts = [
('a\nb', 'title'),
('a\nb', 'title'),
('a\nb', 'title'),
('a\nb', 'title'),
]

def Remake_All_Posts():
    connection = startConnection("database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM posts;")

    UsersInfos = cursor.execute("SELECT id FROM users;").fetchall()
    print(UsersInfos)

    for content in posts:
        if len(content) == 2:
            cursor.execute("INSERT INTO posts (author,title,content) VALUES ("+str(random.choice(UsersInfos)[0])+", '"+content[1]+"', '"+content[0]+"');")
        else:
            cursor.execute("INSERT INTO posts (author,title,content) VALUES ("+str(content[2])+", '"+content[1]+"', '"+content[0]+"');")

    connection.commit()
    connection.close()


Remake_All_Posts()"""