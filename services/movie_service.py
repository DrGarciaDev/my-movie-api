from models.movieModel import MovieModel

class MovieService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        registros = self.db.query(MovieModel).all()
        return registros
    
    def get_movie(self, id):
        registro = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return registro