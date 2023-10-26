from enum import Enum

class CategoryName(str, Enum):
    accion = 'Acción'
    comedia = 'comedia'
    romance = 'Romance'
    terror = 'Terror'
    suspenso = 'Suspenso'