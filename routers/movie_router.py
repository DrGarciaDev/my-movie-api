from fastapi import APIRouter
from typing import Optional, List

from fastapi import Path, Query, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field

# modulos locales
from config.database import Session
from models.movieModel import MovieModel
from middlewares.jwt_bearer import JWTBearer
from services.movie_service import MovieService
from schemas.movie_schema import Movie


movie_router = APIRouter()

@movie_router.get(path='/movies', tags=['Movies'], response_model=List[Movie], status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    registros = MovieService(db).get_movies()

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(registros))

@movie_router.get(path='/movies/{id}', tags=['Movies'], response_model=Movie, status_code=status.HTTP_200_OK)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    registro = MovieService(db).get_movie(id=id)

    if not registro:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No encontrado"})
        
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(registro))

@movie_router.get(path='/movies/', tags=['Movies'], response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    registros = db.query(MovieModel).filter(MovieModel.category == category).all()

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(registros))

@movie_router.post(path='/movies', tags=['Movies'], response_model=dict, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie=movie)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "La pelicula se ha registrado"})

@movie_router.put(path='/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK)
def update_movie(id:  int, movie: Movie) -> dict:
    db = Session()
    registro = MovieService(db=db).get_movie(id=id)

    if not registro:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No encontrado"})

    MovieService(db).update_movie(id=id, data=movie)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "La pelicula se ha editado"})

@movie_router.delete(path='/movies/{id}', tags=['Movies'], response_model=dict, status_code=status.HTTP_200_OK)
def delete_movie(id: int) -> dict:
    db = Session()
    registro = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not registro:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No encontrado"})

    db.delete(registro)
    db.commit()
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "La pelicula se ha eliminado"})