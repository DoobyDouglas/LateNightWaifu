from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi import Depends
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from data_base.data import AnimeDB, DirectorDB, ProfileDB
from .schemas import Anime, RatingRequest, PostAnime
from data_base.models import User
from user.user import current_active_user
from const import VALID_IMAGE_EXT
from messages import (
    EXISTS,
    SORT_TYPES,
    NOT_EXISTS,
    IMAGE_EXT,
    NO_GENRES,
    POST_ANIME_HELP,
    BAD_SORT_KEY,
)
from types import FunctionType
from threading import Thread
from worker.tasks import save_video_util
ANIME_ROUTER = APIRouter(prefix='/anime', tags=['anime'])


@ANIME_ROUTER.get('/', response_model=list[Anime], description=SORT_TYPES)
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
    try:
        return await AnimeDB.get_anime_list(**kwargs)
    except KeyError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, BAD_SORT_KEY)


@ANIME_ROUTER.get('/{anime_id}', response_model=Anime)
async def get_anime(anime_id: int):
    try:
        return await AnimeDB.get_anime(anime_id)
    except AttributeError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, NOT_EXISTS)


@ANIME_ROUTER.post('/', response_model=Anime, description=POST_ANIME_HELP)
async def post_anime(
        anime: PostAnime,
        user: User = Depends(current_active_user)
        ):
    author = await ProfileDB.get_profile(user)
    kwargs = {
        'title': anime.title,
        'director_id': anime.director_id,
        'genres': anime.genres,
        'release_date': anime.release_date,
        'author': author
    }
    try:
        queryset = await AnimeDB.post_anime(**kwargs)
        if isinstance(queryset, str):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, queryset)
        return queryset
    except (UniqueViolation, IntegrityError):
        raise HTTPException(status.HTTP_409_CONFLICT, EXISTS)
    except IndexError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, NO_GENRES)


@ANIME_ROUTER.patch('/{anime_id}', response_model=Anime)
async def add_anime_media(
        anime_id: int,
        poster: UploadFile = File,
        trailer: UploadFile = File,
        user: User = Depends(current_active_user)
        ):
    profile = await ProfileDB.get_profile(user)
    anime = await AnimeDB.get_anime(anime_id)
    if anime.author.id == profile.id:
        if not isinstance(poster, FunctionType):
            try:
                if poster.content_type not in VALID_IMAGE_EXT:
                    raise HTTPException(
                        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, IMAGE_EXT
                    )
                kwargs = {
                    'anime_id': anime_id,
                    'poster': poster,
                }
                await AnimeDB.save_image(**kwargs)
            except AttributeError:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, NOT_EXISTS)
        if not isinstance(trailer, FunctionType):
            thread = Thread(target=save_video_util, args=(anime.title, anime_id, trailer.filename, trailer))
            thread.start()
        anime.trailer = 'Загружается'
        return anime


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
        raise HTTPException(status.HTTP_400_BAD_REQUEST, NOT_EXISTS)


DIRECTOR_ROUTER = APIRouter(prefix='/director', tags=['director'])


@DIRECTOR_ROUTER.get('/', description=SORT_TYPES)
async def get_director_list(
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
        return await DirectorDB.get_director_list(**kwargs)
    except KeyError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, BAD_SORT_KEY)


@DIRECTOR_ROUTER.post('/',)
async def post_director(name: str, user: User = Depends(current_active_user)):
    try:
        return await DirectorDB.add_director(name)
    except (UniqueViolation, IntegrityError):
        raise HTTPException(status.HTTP_409_CONFLICT, EXISTS)


if __name__ == '__main__':
    pass
