from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from data_base.data import AnimeDB, DirectorDB, ProfileDB, GenreDB
from .schemas import Anime, RatingRequest, PostAnime
from data_base.models import User
from user.user import current_active_user
from settings import (
    VALID_IMAGE_EXT,
    API_PREFIX,
    MAX_UPLOAD_IMAGE_SIZE,
    MAX_UPLOAD_VIDEO_SIZE,
)
from messages import (
    EXISTS,
    SORT_TYPES,
    NOT_EXISTS,
    IMAGE_EXT,
    NO_GENRES,
    POST_ANIME_HELP,
    BAD_SORT_KEY,
    BIG_FILESIZE,
)
from types import FunctionType
from threading import Thread
from worker.tasks import save_video_util
from fastapi.exceptions import ResponseValidationError
from anyio import EndOfStream

ANIME_ROUTER = APIRouter(prefix=f'{API_PREFIX}/anime', tags=['anime'])
DIRECTOR_ROUTER = APIRouter(prefix=f'{API_PREFIX}/director', tags=['director'])
GENRE_ROUTER = APIRouter(prefix=f'{API_PREFIX}/genre', tags=['genre'])


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
        anime = await AnimeDB.get_anime(anime_id)
        if not anime:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, NOT_EXISTS)
        return anime
    except (AttributeError, ResponseValidationError, EndOfStream):
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
        'description': anime.description,
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
        user: User = Depends(current_active_user),
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
                if poster.size > MAX_UPLOAD_IMAGE_SIZE:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, BIG_FILESIZE
                    )
                kwargs = {
                    'anime_id': anime_id,
                    'poster': poster,
                }
                await AnimeDB.save_image(**kwargs)
                anime = await AnimeDB.get_anime(anime_id)
            except AttributeError:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, NOT_EXISTS)
        if not isinstance(trailer, FunctionType):
            if trailer.size > MAX_UPLOAD_VIDEO_SIZE:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, BIG_FILESIZE
                )
            Thread(
                target=save_video_util,
                args=(anime.title, anime_id, trailer.filename, trailer)
            ).start()
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


@DIRECTOR_ROUTER.get('/')
async def get_director_list(
    offset: int = 0,
    limit: int = 10,
        ):
    kwargs = {
        'offset': offset,
        'limit': limit,
    }
    return await DirectorDB.get_director_list(**kwargs)
    # сделать обрабокту на возможные ошибки


@DIRECTOR_ROUTER.post('/',)
async def post_director(name: str, user: User = Depends(current_active_user)):
    try:
        return await DirectorDB.add_director(name)
    except (UniqueViolation, IntegrityError):
        raise HTTPException(status.HTTP_409_CONFLICT, EXISTS)


@GENRE_ROUTER.get('/')
async def get_genre_list(
    offset: int = 0,
    limit: int = 10,
        ):
    kwargs = {
        'offset': offset,
        'limit': limit,
    }
    return await GenreDB.get_genre_list(**kwargs)
    # сделать обрабокту на возможные ошибки


@GENRE_ROUTER.post('/',)
async def post_genre(name: str, user: User = Depends(current_active_user)):
    try:
        return await GenreDB.add_genre(name)
    except (UniqueViolation, IntegrityError):
        raise HTTPException(status.HTTP_409_CONFLICT, EXISTS)


if __name__ == '__main__':
    pass
