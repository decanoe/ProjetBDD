import sqlite3

connexion = sqlite3.connect("database.db")
cur = connexion.cursor()
req = "INSERT INTO users (login,password,email,age) VALUES ('erwan2511','test','erwan.legrand@gmail.com',17)"
cur.execute(req)
connexion.commit()
connexion.close()