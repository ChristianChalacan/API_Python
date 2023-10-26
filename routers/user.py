from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import APIRouter

from utils.jwt_manager import create_token

from schemas.user import User

user_router = APIRouter()

#Ruta de Inicio de sesion
@user_router.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
    return JSONResponse(status_code=200 ,content=token)