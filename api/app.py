from fastapi import FastAPI
from user.schemas import UserCreate, UserRead, UserUpdate
from fastapi.staticfiles import StaticFiles
from user.user import auth_backend, fastapi_users
from api.routers import ANIME_ROUTER, DIRECTOR_ROUTER, GENRE_ROUTER
from frontend.routers import FRONTEND_ROUTER
from settings import API_PREFIX


LATE_NIGHT_WAIFU = FastAPI()

LATE_NIGHT_WAIFU.mount(
    '/static', StaticFiles(directory='static'), name='static'
)
LATE_NIGHT_WAIFU.mount(
    '/media', StaticFiles(directory='media'), name='media'
)

LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"{API_PREFIX}/auth/jwt",
    tags=["auth"],
)
LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=f"{API_PREFIX}/auth",
    tags=["auth"],
)
LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=f"{API_PREFIX}/auth",
    tags=["auth"],
)
LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix=f"{API_PREFIX}/auth",
    tags=["auth"],
)
LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=f"{API_PREFIX}/users",
    tags=["users"],
)
LATE_NIGHT_WAIFU.include_router(ANIME_ROUTER)
LATE_NIGHT_WAIFU.include_router(DIRECTOR_ROUTER)
LATE_NIGHT_WAIFU.include_router(GENRE_ROUTER)
LATE_NIGHT_WAIFU.include_router(FRONTEND_ROUTER)


if __name__ == '__main__':
    pass
