from fastapi import APIRouter
from data_base.data import AnimeDB
from .schemas import Anime, AddAnime, RatingRequest
from fastapi import Depends
from data_base.models import User
from user.user import current_active_user
from typing import Union

anime_router = APIRouter(prefix='/anime', tags=['anime'])


@anime_router.get('/', response_model=list[Anime])
async def get_anime_list(
        offset: int = 0,
        limit: int = 10,
        ordering: str = None,
        ):
    kwargs = {
        'offset': offset,
        'limit': limit,
        'ordering': ordering,
    }
    return await AnimeDB.get_anime_list(**kwargs)


@anime_router.post(
    '/', response_model=Union[AddAnime, None],
    description='В теле запроса должен присутствовать массив из id жанров'
)
async def post_anime(
        title: str,
        director_id: int,
        genres: list[int],
        user: User = Depends(current_active_user)
        ):
    kwargs = {
        'title': title,
        'director_id': director_id,
        'genres': genres,
    }
    return await AnimeDB.add_anime(**kwargs)


@anime_router.get('/{anime_id}', response_model=Union[Anime, None])
async def get_anime(anime_id: int):
    return await AnimeDB.get_anime(anime_id)


@anime_router.post('/{anime_id}/rate')
async def rate_anime(
        anime_id: int,
        rate: RatingRequest,
        user: User = Depends(current_active_user)
        ):
    kwargs = {
        'anime_id': anime_id,
        'rate': rate.rate,
        'user_id': user.id,
    }
    return await AnimeDB.rate_anime(**kwargs)


if __name__ == '__main__':
    pass
