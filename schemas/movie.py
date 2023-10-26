from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class Movie(BaseModel):
    #A traves de Typing declaramos un valor opcional con su tipo de dato
    id: Optional[int] = None
    #Con Pydantic agregamos una validacion de longitud
    title: str = Field(min_length=5,max_length=15)
    overview: str = Field(min_length=15,max_length=50)
    year: int = Field(ge=1999,le=date.today().year)
    rating: float = Field(ge=0,le=10)
    category: str = Field(min_length=5, max_length=15)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }