from models.movieModel import MovieModel
from schemas.movie_schema import Movie

class MovieService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        registros = self.db.query(MovieModel).all()
        return registros
    
    def get_movie(self, id):
        registro = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return registro
    
    def get_movies_by_category(self, category):
        registros = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return registros
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())

        self.db.add(new_movie)
        self.db.commit()

        return
    
    def update_movie(self, id: int, data: Movie):
        registro = self.db.query(MovieModel).filter(MovieModel.id == id).first()

        registro.title = data.title
        registro.overview = data.overview
        registro.year = data.year
        registro.category = data.category
        registro.rating = data.rating

        self.db.commit()

        return
    
    def delete_movie(self, id: int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()

        return 