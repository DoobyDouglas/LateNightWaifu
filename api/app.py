from fastapi import FastAPI
from user.schemas import UserCreate, UserRead, UserUpdate
from user.user import auth_backend, fastapi_users
from api.routers import ANIME_ROUTER, DIRECTOR_ROUTER


LATE_NIGHT_WAIFU = FastAPI()

LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
LATE_NIGHT_WAIFU.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
LATE_NIGHT_WAIFU.include_router(ANIME_ROUTER)
LATE_NIGHT_WAIFU.include_router(DIRECTOR_ROUTER)
