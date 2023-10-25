from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from enum import Enum

from pydantic import BaseModel, Field

from typing import Optional, List

#Librerias Opcionales
from datetime import date

#Importando token
from jwt_manager import create_token, validate_token

#Importar para validar seguridad
from fastapi.security import HTTPBearer



#Podemos crear constantes para recibir datos especificos
#La clase recibe dos parametros el primero hace referencia al tipo de dato que retornara
#y el segundo es la herencia hacia Enum
class CategoryName(str, Enum):
    accion = 'Acción'
    comedia = 'comedia'
    romance = 'Romance'
    terror = 'Terror'
    suspenso = 'Suspenso'
    
class IdMovie(str, Enum):
    uno = '1'
    dos = '2'
    
class Item(BaseModel):
    #A traves de Typing declaramos un valor opcional con su tipo de dato
    id: Optional[int] = None
    #Con Pydantic agregamos una validacion de longitud
    title: str = Field(default='Pelicula',min_length=5,max_length=15)
    overview: str = Field(default='Descripcion',min_length=15,max_length=50)
    year: int = Field(default=1955 ,ge=1999,le=date.today().year)
    rating: float = Field(ge=0,le=10)
    category: str
    

#Iniciamos una instancia de FastAPI
app = FastAPI()
#Agregamos un titulo a nuestra API
app.title = 'Mi API con FastAPI'
#Agregamos la version de nuestra API
app.version = '0.0.1'

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="invalid credential")

class User(BaseModel):
    email: str
    password: str


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2022',
        'rating': 9.2,
        'category': 'Acción'    
    },
    {
        'id': 3,
        'title': 'Avatar 3',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2022',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 4,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2021',
        'rating': 9.2,
        'category': 'Comedia'    
    },
    {
        'id': 5,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2010',
        'rating': 7.8,
        'category': 'Romance'    
    },
    {
        'id': 6,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2022',
        'rating': 9.2,
        'category': 'Terror'    
    },
    {
        'id': 7,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Suspenso'    
    },
    {
        'id': 8,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2022',
        'rating': 9.2,
        'category': 'Acción'    
    }
]

#Desplegamos un HTML
@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')

#Ruta de Inicio de sesion
@app.post('/login', tags=['Auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
    return JSONResponse(status_code=200 ,content=token)


#Retornamos todas las peliculas
@app.get('/movies', tags=['Movies'], response_model=List[Item], status_code=200, dependencies=[Depends(JWTBearer)])
def get_movies() -> List[Item]:
    return JSONResponse(status_code=200,content=movies)

#Retornamos una pelicula con un id en especifico
#usamos el metodo Path para validar los parametros de ruta
@app.get('/movies/{id}', tags=['Movies'], response_model=List[Item])
def get_movie(id: int =Path(ge=1, le=2000)) -> List[Item]:
    return JSONResponse(content=list(filter(lambda movie: movie['id'] == id,movies)))

#Retornamos las peliculas con una categoria en especifico
#Para añadir un parámetro query se agrega / al final de la ruta
@app.get('/movies/', tags=['Movies'], response_model=List[Item])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Item]:
    data = list(filter(lambda movie: movie['category'] == category, movies)) 
    return JSONResponse(content=data)

#@app.get('/movies/', tags=['Movies'])
#def get_movies_by_year(name: str, year: int):
#    return list(filter(lambda movie: int(movie['year']) == year,movies))

#Creamos una nueva pelicula sin BaseModel
@app.post('/movies', tags = ['Movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: str = Body(), rating: float = Body(), category: str  = Body()):
    movies.append({
        'id':id,
        'title':title,
        'overview':overview,
        'year':year,
        'rating':rating,
        'category':category
    })
    return movies

#Creamos una nueva pelicula con BaseModel
@app.post('/movies/BaseModel', tags=['Movies/BaseModel'], response_model=dict, status_code=201)
async def create_movie_BaseModel(item: Item) -> dict:
    movies.append(item)
    return JSONResponse(status_code=201 ,content={"code":1 ,"message": "Exitoso"})
    
#Uso de Enum para control de datos con constantes
@app.get('/movies/category/{category_name}', tags=['Movies/Categories'])
async def get_movies_by_category_enum(category_name: CategoryName):
    return category_name
    
#Ejemplo de retorno de tipos de datos con Enum
@app.get('/movies/id/{id}', tags=['Movies Id'])
async def get_movie_by_id_enum(id: IdMovie):
    if id is IdMovie.uno:
        return IdMovie.uno
    if id is IdMovie.dos:
        return IdMovie.dos
    
#Actualiza registro
@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, item: Item) -> dict:
    for item_movies in movies:
        if item_movies['id'] == id:
            item_movies['title'] = item.title
            item_movies['overview'] = item.overview
            item_movies['year'] = item.year
            item_movies['rating'] = item.rating
            item_movies['category'] = item.category
    return JSONResponse(status_code=200 ,content={"code":2 ,"message": "Exitoso"})
      
#Elimina Registros            
@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    return JSONResponse(status_code=200,content={"code":3 ,"message": "Exitoso"})
            