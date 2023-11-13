from fastapi import APIRouter, File, UploadFile, HTTPException, status
from data_base.data import AnimeDB, DirectorDB, ProfileDB
from .schemas import Anime, RatingRequest, PostAnime
from fastapi import Depends
from data_base.models import User
from user.user import current_active_user
from typing import Union
from const import POSTERS_FORMATS
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError


ANIME_ROUTER = APIRouter(prefix='/anime', tags=['anime'])


@ANIME_ROUTER.get(
        '/',
        response_model=list[Anime],
        description='Сортировка по "rating_desc" и "rating_asc"'
)
async def get_anime_list(
        offset: int = 0,
        limit: int = 10,
        ordering: str = None,
        ):
    try:
        kwargs = {
            'offset': offset,
            'limit': limit,
            'ordering': ordering,
        }
        return await AnimeDB.get_anime_list(**kwargs)
    except KeyError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Несуществующий ключ для сортировки'
        )


@ANIME_ROUTER.get('/{anime_id}', response_model=Anime)
async def get_anime(anime_id: int):
    try:
        return await AnimeDB.get_anime(anime_id)
    except AttributeError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Аниме с таким id не существует в базе'
        )


@ANIME_ROUTER.post(
    '/', response_model=Anime,
    description=(
        'Жанры добавляются по их id. '
        'Дата в формате 2023-11-13T15:50:24.936Z'
    )
)
async def post_anime(
        anime: PostAnime,
        user: User = Depends(current_active_user)
        ):
    try:
        author = await ProfileDB.get_profile(user)
        kwargs = {
            'title': anime.title,
            'director_id': anime.director_id,
            'genres': anime.genres,
            'date': anime.date,
            'author': author
        }
        queryset = await AnimeDB.add_anime(**kwargs)
        if not queryset:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Жанра с таким id или режиссёра не существует в базе'
            )
        return queryset
    except (UniqueViolation, IntegrityError):
        raise HTTPException(
                status.HTTP_409_CONFLICT,
                'Такая запись уже существует в базе'
        )
    except IndexError:
        raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Добавьте один или несколько жанров'
        )


@ANIME_ROUTER.post('/{anime_id}', response_model=Union[Anime, None])
async def add_anime_media(
        anime_id: int,
        poster: UploadFile = File(...),
        user: User = Depends(current_active_user)
        ):
    try:
        if poster.content_type not in POSTERS_FORMATS:
            raise HTTPException(
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                'Для постеров используются файлы форматов jpeg и png'
            )
        profile = await ProfileDB.get_profile(user)
        kwargs = {
            'anime_id': anime_id,
            'poster': poster,
            'profile': profile,
        }
        return await AnimeDB.save_image(**kwargs)
    except AttributeError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Аниме с таким id не существует в базе'
        )


@ANIME_ROUTER.post('/{anime_id}/rate')
async def rate_anime(
        anime_id: int,
        rate: RatingRequest,
        user: User = Depends(current_active_user)
        ):
    try:
        profile = await ProfileDB.get_profile(user)
        kwargs = {
            'anime_id': anime_id,
            'rate': rate.rate,
            'profile_id': profile.id,
        }
        return await AnimeDB.rate_anime(**kwargs)
    except AttributeError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Аниме с таким id не существует в базе'
        )


DIRECTOR_ROUTER = APIRouter(prefix='/director', tags=['director'])


@DIRECTOR_ROUTER.get(
        '/',
        description='Сортировка по "rating_desc" и "rating_asc"'
)
async def get_director_list(
    offset: int = 0,
    limit: int = 10,
    ordering: str = None,
        ):
    kwargs = {
        'offset': offset,
        'limit': limit,
        'ordering': ordering,
    }
    return await DirectorDB.get_director_list(**kwargs)


@DIRECTOR_ROUTER.post('/',)
async def post_director(name: str, user: User = Depends(current_active_user)):
    try:
        return await DirectorDB.add_director(name)
    except (UniqueViolation, IntegrityError):
        raise HTTPException(
                status.HTTP_409_CONFLICT,
                'Такая запись уже существует в базе'
        )


if __name__ == '__main__':
    pass
