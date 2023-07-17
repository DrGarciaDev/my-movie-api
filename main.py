from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = 'Mi app con FastAPI'
app.version = '0.0.1'

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
def get_movie(id: int):
    for item in movies:
        if item['id'] == id:
            return item
        
    return []

@app.get(path='/movies/', tags=['Movies'])
def get_movies_by_category(category: str, year: int):
    return category