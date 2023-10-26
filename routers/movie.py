from enum import Enum
from typing import List
from fastapi import APIRouter, Body, Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.database import Session
from middlewares.jwt_bearer import JWTBearer

from models.movie import Movie as MovieModel
#Importando servicios
from services.movie import MovieService
#Importando esquemas
from schemas.category_name import CategoryName
from schemas.movie import Movie


movie_router = APIRouter()

#Ejemplo
class IdMovie(str, Enum):
    uno = '1'
    dos = '2'
    

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }
]
    
#Retornamos todas las peliculas
@movie_router.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer)])
def get_movies() -> List[Movie]:
    db = Session()
    data = MovieService(db).get_movies()
    if not data:
        return JSONResponse(status_code=404, content={"message": "No se encontraron registros"})
    return JSONResponse(status_code=200,content=jsonable_encoder(data))

#Retornamos una pelicula con un id en especifico
#usamos el metodo Path para validar los parametros de ruta
@movie_router.get('/movies/{id}', tags=['Movies'], response_model=List[Movie])
def get_movie(id: int =Path(ge=1, le=2000)) -> List[Movie]:
    db = Session()
    data = MovieService(db).get_movie_by_id(id)
    if not data:
        return JSONResponse(status_code=404, content={"message": "No se encontro registro"})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

#Retornamos las peliculas con una categoria en especifico
#Para añadir un parámetro query se agrega / al final de la ruta
@movie_router.get('/movies/', tags=['Movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    data = MovieService(db).get_movie_by_category(category)
    #data = list(filter(lambda movie: movie['category'] == category, movies)) 
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

#@app.get('/movies/', tags=['Movies'])
#def get_movies_by_year(name: str, year: int):
#    return list(filter(lambda movie: int(movie['year']) == year,movies))

#Creamos una nueva pelicula sin BaseModel
@movie_router.post('/movies', tags = ['Movies'])
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
@movie_router.post('/movies/BaseModel', tags=['Movies/BaseModel'], response_model=dict, status_code=201)
async def create_movie_BaseModel(item: Movie) -> dict:
    db = Session()
    response = MovieService(db).create_movie(MovieModel(**item.dict()))
    if response:
        return JSONResponse(status_code=201 ,content={"code":1 ,"message": "Exitoso"})
    
#Uso de Enum para control de datos con constantes
@movie_router.get('/movies/category/{category_name}', tags=['Movies/Categories'])
async def get_movies_by_category_enum(category_name: CategoryName):
    return category_name
    
#Ejemplo de retorno de tipos de datos con Enum
@movie_router.get('/movies/id/{id}', tags=['Movies Id'])
async def get_movie_by_id_enum(id: IdMovie):
    if id is IdMovie.uno:
        return IdMovie.uno
    if id is IdMovie.dos:
        return IdMovie.dos
    
#Actualiza registro
@movie_router.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, item: Movie) -> dict:
    db = Session()
    response = MovieService(db).update_movie(id, item)
    if not response:
        return JSONResponse(status_code=404, content={"message": "No se encontro registro"})
    return JSONResponse(status_code=200 ,content={"code":2 ,"message": "Exitoso"})
      
#Elimina Registros            
@movie_router.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    response = MovieService(db).delete_movie(id)
    if not response:
        return JSONResponse(status_code=404, content={"message": "No se encontro registro"})
    return JSONResponse(status_code=200,content={"code":3 ,"message": "Exitoso"})