from multiprocessing import connection
import _sqlite3
from app import startConnection

connection = startConnection("database.db")
cur = connection.cursor()

req = "DELETE FROM comments"
cur.execute(req)
connection.commit()
connection.close()