from typing import Optional

from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse

from pydantic import BaseModel, Field

app = FastAPI()
app.title = 'Mi app con FastAPI'
app.version = '0.0.1'

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripción de la película",
                "year": 2022, 
                "rating": 9.8,
                "category": "Categoría"
            }
        }


movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get(path='/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.get(path='/movies', tags=['Movies'])
def get_movies():
    return movies

@app.get(path='/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item['id'] == id:
            return item
        
    return []

@app.get(path='/movies/', tags=['Movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return [ item for item in movies if item['category'] == category ]

@app.post(path='/movies', tags=['Movies'])
def create_movie(movie: Movie):
    movies.append(movie)

    return movies

@app.put(path='/movies/{id}', tags=['Movies'])
def update_movie(id:  int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['category'] = movie.category
            item['rating'] = movie.rating
    
    return movies

@app.delete(path='/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    
    return movies