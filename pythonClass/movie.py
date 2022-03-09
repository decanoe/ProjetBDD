class Movie:
    def __init__(self,id, title, realisator, date, duration, image_path, genres, resum, resum_author, resum_author_id, creation_date):
        self.id = id
        self.title = title
        self.realisator = realisator
        self.date = date
        self.duration = duration
        self.image_path = image_path
        self.genres = genres
        self.resum = resum
        self.resum_author = resum_author
        self.resum_author_id = resum_author_id
        self.creation_date = creation_date