from .psycopg2_connection import ENGINE
from .models import Director, Anime, Genre, User_Anime_Rating
from sqlalchemy.orm import sessionmaker
from typing import Union
from data_base.models import User


class AnimeDB:

    __SESSION = sessionmaker(ENGINE)

    @classmethod
    async def get_anime_list(
            cls,
            offset: int = 0,
            limit: int = 10
            ) -> list[Anime]:
        with cls.__SESSION() as session:
            anime_list = session.query(Anime).all()[offset:][:limit]
            for anime in anime_list:
                anime.genres
                anime.director
        return anime_list

    @classmethod
    async def get_anime(cls, anime_id: int) -> Union[Anime, None]:
        with cls.__SESSION() as session:
            anime = session.query(Anime).where(Anime.id == anime_id).first()
            if not anime:
                return None
            anime.genres
            anime.director
        return anime

    @classmethod
    async def add_anime(
        cls,
        title: str,
        director_id: int,
        genres: list[int]
            ) -> Anime:
        with cls.__SESSION() as session:
            director = session.query(Director).where(
                Director.id == director_id
            ).first()
            genres = session.query(Genre).filter(Genre.id.in_(genres)).all()
            anime = Anime(title=title, director=director, genres=genres)
            session.add(anime)
            session.commit()
            anime = session.query(Anime).where(Anime.id == anime.id).first()
            anime.genres
            anime.director
        return anime

    @classmethod
    async def rate_anime(cls, user: User, anime_id: int, rate: int) -> Anime:
        with cls.__SESSION() as session:
            anime = session.query(Anime).where(Anime.id == anime_id).first()
            rating = session.query(User_Anime_Rating).where(User_Anime_Rating.anime_id == anime_id, User_Anime_Rating.user_id == user.id).first()
            if not rating:
                anime.rating_count += 1
                anime.rating += (rate - anime.rating) / anime.rating_count
                rating = User_Anime_Rating(anime_id=anime_id, user_id=user.id, rating=rate)
                session.add(rating)
            session.commit()
            anime = session.query(Anime).where(Anime.id == anime.id).first()
            anime.genres
            anime.director
        return anime
