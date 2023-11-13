from .psycopg2_connection import ENGINE
from .models import Director, Anime, Genre, Profile_Anime_Rating, Profile, User
from sqlalchemy.orm import sessionmaker
from fastapi import UploadFile
import os
from settings import MEDIA_DIR
import shutil
from slugify import slugify


_ORDER_DICT = {
    None: None,
    'rating_desc': Anime.rating.desc(),
    'rating_asc': Anime.rating.asc(),
}


class BaseDB:

    _SESSION = sessionmaker(ENGINE)


class AnimeDB(BaseDB):

    @classmethod
    async def get_anime_list(cls, **kwargs) -> list[Anime]:
        with cls._SESSION() as session:
            anime_list = session.query(Anime).order_by(
                _ORDER_DICT[kwargs['ordering']]
            ).all()[kwargs['offset']:][:kwargs['limit']]
            for anime in anime_list:
                anime.genres
                anime.director
        return anime_list

    @classmethod
    async def get_anime(cls, anime_id: int) -> Anime | None:
        with cls._SESSION() as session:
            anime = session.get(Anime, anime_id)
            anime.genres
            anime.director
            anime.author
            anime.poster
        return anime

    @classmethod
    async def add_anime(cls, **kwargs) -> Anime | None:
        with cls._SESSION() as session:
            kwargs['director'] = session.query(Director).where(
                Director.id == kwargs.pop('director_id')
            ).first()
            kwargs['genres'] = session.query(Genre).filter(
                Genre.id.in_(kwargs['genres'])
            ).all()
            if not kwargs['director'] or not kwargs['genres']:
                return None
            anime = Anime(**kwargs)
            session.add(anime)
            session.commit()
            anime = session.get(Anime, anime.id)
            anime.genres
            anime.director
        return anime

    @classmethod
    async def save_image(cls, **kwargs) -> str:
        poster: UploadFile
        poster = kwargs['poster']
        anime = await cls.get_anime(kwargs['anime_id'])
        profile = kwargs['profile']
        if anime.author.id == profile.id:
            slug_title = slugify(anime.title)
            filename = f'{slug_title}{os.path.splitext(poster.filename)[-1]}'
            title_dir = os.path.join(MEDIA_DIR, slug_title)
            path = os.path.join(title_dir, filename)
            os.makedirs(title_dir, exist_ok=True)
            with open(path, 'wb') as file:
                shutil.copyfileobj(poster.file, file)
            with cls._SESSION() as session:
                anime = session.get(Anime, kwargs['anime_id'])
                anime.poster = path
                session.commit()
                anime = session.get(Anime, kwargs['anime_id'])
                anime.director
                anime.genres
            return anime

    @classmethod
    async def rate_anime(cls, **kwargs) -> Anime:
        with cls._SESSION() as session:
            anime_id, profile_id = kwargs['anime_id'], kwargs['profile_id']
            anime = session.get(Anime, anime_id)
            rating = session.query(
                Profile_Anime_Rating
            ).filter(
                Profile_Anime_Rating.anime_id == anime_id,
                Profile_Anime_Rating.profile_id == profile_id
            ).first()
            if not rating:
                rate = kwargs['rate']
                anime.rating_count += 1
                anime.rating += (rate - anime.rating) / anime.rating_count
                rating = Profile_Anime_Rating(
                    anime_id=anime_id, profile_id=profile_id, rating=rate
                )
                session.add(rating)
            session.commit()
            anime = session.get(Anime, anime.id)
            anime.genres
            anime.director
        return anime


class DirectorDB(BaseDB):

    @classmethod
    async def get_director_list(cls, **kwargs) -> list[Director]:
        with cls._SESSION() as session:
            director_list = session.query(Director).order_by(
                _ORDER_DICT[kwargs['ordering']]
            ).all()[kwargs['offset']:][:kwargs['limit']]
            for director in director_list:
                director.anime_list
        return director_list

    @classmethod
    async def add_director(cls, name) -> Director:
        with cls._SESSION() as session:
            director = Director(name=name)
            session.add(director)
            session.commit()
            director = session.get(Director, director.id)
        return director


class ProfileDB(BaseDB):

    @classmethod
    async def get_profile(cls, user: User) -> Profile:
        with cls._SESSION() as session:
            profile = session.query(
                Profile
            ).filter(Profile.user_id == user.id).first()
            return profile
