from pydantic import BaseModel, Field


class Genre(BaseModel):

    name: str


class Director(BaseModel):

    name: str


class Anime(BaseModel):

    title: str
    genres: list[Genre]
    director: Director
    rating: float


class AddAnime(Anime):
    id: int


class RatingRequest(BaseModel):
    rate: int = Field(..., ge=0, le=10)
