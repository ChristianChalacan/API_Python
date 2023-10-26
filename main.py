from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from pydantic import BaseModel

#Importa los datos de la base
from config.database import engine, Base

#Manejo de errores
from middlewares.error_handler import ErrorHandler

#Podemos crear constantes para recibir datos especificos
#La clase recibe dos parametros el primero hace referencia al tipo de dato que retornara
#y el segundo es la herencia hacia Enum

#Adicion de Router para el apartado de peliculas
from routers.movie import movie_router
from routers.user import user_router

#Iniciamos una instancia de FastAPI
app = FastAPI()
#Agregamos un titulo a nuestra API
app.title = 'Mi API con FastAPI'
#Agregamos la version de nuestra API
app.version = '0.0.1'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind = engine)

#Desplegamos un HTML
@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')


            