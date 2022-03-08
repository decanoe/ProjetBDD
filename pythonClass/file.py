from fileinput import filename
from werkzeug.utils import secure_filename
import os

class File():
    def __init__(self,file):
        self.file = file

    def save_file(self):
        file_name = secure_filename(self.file.filename)
        self.file.save("movies/"+file_name)

    def get_filename(self):
        file_name = secure_filename(self.file.filename)
        return file_name