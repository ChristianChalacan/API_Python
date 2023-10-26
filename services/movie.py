from models.movie import Movie
from config.database import Session

class MovieService():
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def get_movies(self):
        data = self.db.query(Movie).all()
        return data
    
    def get_movie_by_id(self, id: int):
        data = self.db.query(Movie).filter(Movie.id == id).first()
        return data
    
    def get_movie_by_category(self, category: str):
        data = self.db.query(Movie).filter(Movie.category == category).all()
        return data
    
    def create_movie(self, movie: Movie):
        self.db.add(movie)
        self.db.commit()
        return True
    
    def update_movie(self, id, new_data):
        data = self.db.query(Movie).filter(Movie.id == id).first()
        if not data:
            return False
        data.title = new_data.title
        data.overview = new_data.overview
        data.year = new_data.year
        data.rating = new_data.rating
        data.category = new_data.category
        self.db.commit()
        return True

    def delete_movie(self, id: int):
        data = self.db.query(Movie).filter(Movie.id == id).first()
        if not data:
            return False
        self.db.delete(data)
        self.db.commit()
        return True
        
        