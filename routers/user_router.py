from pydantic import BaseModel

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

# modulos locales 
from jwt_manager import create_token


user_router = APIRouter()

class User(BaseModel):
    email: str
    password: str 


@user_router.post(path='/login', tags=['Auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())

    return JSONResponse(status_code=status.HTTP_200_OK, content=token)