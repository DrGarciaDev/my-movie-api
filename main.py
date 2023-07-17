from fastapi import FastAPI, Body
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
    return [ item for item in movies if item['category'] == category ]

@app.post(path='/movies', tags=['Movies'])
def create_movie(id:  int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), category: str = Body(), rating: float = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })

    return movies

@app.put(path='/movies/{id}', tags=['Movies'])
def update_movie(id:  int, title: str = Body(), overview: str = Body(), year: int = Body(), category: str = Body(), rating: float = Body()):
    for item in movies:
        if item['id'] == id:
            item['title'] = title,
            item['overview'] = overview,
            item['year'] = year,
            item['category'] = category,
            item['rating'] = rating
    
    return movies

@app.delete(path='/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    
    return movies