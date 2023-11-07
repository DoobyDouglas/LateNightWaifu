from .psycopg2_connection import ENGINE
from .models import Director, Anime, Genre, User_Anime_Rating
from sqlalchemy.orm import sessionmaker


_ORDER_DICT = {
    None: None,
    'rating_desc': Anime.rating.desc(),
    'rating_asc': Anime.rating.asc(),
}


class AnimeDB:

    __SESSION = sessionmaker(ENGINE)

    @classmethod
    async def get_anime_list(cls, **kwargs) -> list[Anime]:
        with cls.__SESSION() as session:
            anime_list = session.query(Anime).order_by(
                _ORDER_DICT[kwargs['ordering']]
            ).all()[kwargs['offset']:][:kwargs['limit']]
            for anime in anime_list:
                anime.genres
                anime.director
        return anime_list

    @classmethod
    async def get_anime(cls, anime_id: int) -> Anime | None:
        with cls.__SESSION() as session:
            anime = session.get(Anime, anime_id)
            if not anime:
                return None
            anime.genres
            anime.director
        return anime

    @classmethod
    async def add_anime(cls, **kwargs) -> Anime | None:
        with cls.__SESSION() as session:
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
    async def rate_anime(cls, **kwargs) -> Anime:
        with cls.__SESSION() as session:
            anime_id, user_id = kwargs['anime_id'], kwargs['user_id']
            anime = session.get(Anime, anime_id)
            rating = session.query(
                User_Anime_Rating
            ).filter(
                User_Anime_Rating.anime_id == anime_id,
                User_Anime_Rating.user_id == user_id
            ).first()
            if not rating:
                rate = kwargs['rate']
                anime.rating_count += 1
                anime.rating += (rate - anime.rating) / anime.rating_count
                rating = User_Anime_Rating(
                    anime_id=anime_id, user_id=user_id, rating=rate
                )
                session.add(rating)
            session.commit()
            anime = session.get(Anime, anime.id)
            anime.genres
            anime.director
        return anime
