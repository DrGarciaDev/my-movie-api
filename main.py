from typing import Optional, List

from fastapi import FastAPI, Body, Path, Query, status, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from pydantic import BaseModel, Field
from starlette.requests import Request

from jwt_manager import create_token, validate_token

app = FastAPI()
app.title = 'Mi app con FastAPI'
app.version = '0.0.1'

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Credenciales son inválidas')
    
    
class User(BaseModel):
    email: str
    password: str 
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

@app.post(path='/login', tags=['Auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())

    return JSONResponse(status_code=status.HTTP_200_OK, content=token)

@app.get(path='/movies', tags=['Movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=status.HTTP_200_OK, content=movies)

@app.get(path='/movies/{id}', tags=['Movies'], response_model=Movie, status_code=status.HTTP_200_OK)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item['id'] == id:
            return JSONResponse(status_code=status.HTTP_200_OK, content=item)
        
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])

@app.get(path='/movies/', tags=['Movies'], response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [ item for item in movies if item['category'] == category ]
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)

@app.post(path='/movies', tags=['Movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "La pelicula se ha registrado"})

@app.put(path='/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id:  int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['category'] = movie.category
            item['rating'] = movie.rating
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "La pelicula se ha editado"})

@app.delete(path='/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "La pelicula se ha eliminado"})