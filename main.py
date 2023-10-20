from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

#Iniciamos una instancia de FastAPI
app = FastAPI()
#Agregamos un titulo a nuestra API
app.title = 'Mi API con FastAPI'
#Agregamos la version de nuestra API
app.version = '0.0.1'

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

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Hello World!</h1>')

@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int):
    return list(filter(lambda movie: movie['id'] == id,movies))

#Para añadir un parámetro query se agrega / al final de la ruta
@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category: str, year: int = 1950):
    return list(filter(lambda movie: movie['category'] == category, movies)) 

#@app.get('/movies/', tags=['Movies'])
#def get_movies_by_year(name: str, year: int):
#    return list(filter(lambda movie: int(movie['year']) == year,movies))

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