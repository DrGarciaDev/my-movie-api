from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse, JSONResponse

from pydantic import BaseModel

# modulos locales
from jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie_router import movie_router

app = FastAPI()
app.title = 'Mi app con FastAPI'
app.version = '0.0.1'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)
    
class User(BaseModel):
    email: str
    password: str 

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