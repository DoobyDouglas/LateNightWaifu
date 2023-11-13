from pydantic import BaseModel, Field
from datetime import date


class Genre(BaseModel):

    id: int
    name: str


class Director(BaseModel):

    id: int
    name: str


class Anime(BaseModel):

    id: int
    title: str
    director: Director
    date: date
    genres: list[Genre]
    rating: float
    poster: str | None


class PostAnime(BaseModel):

    title: str
    director_id: int
    date: date
    genres: list[int]


class RatingRequest(BaseModel):

    rate: int = Field(..., ge=0, le=10)
