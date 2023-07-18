from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# modulos locales
from jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie_router import movie_router
from routers.user_router import user_router

app = FastAPI()
app.title = 'Mi app con FastAPI'
app.version = '0.0.1'

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)

@app.get(path='/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

app.include_router(user_router)
app.include_router(movie_router)