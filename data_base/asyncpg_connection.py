from settings import POSTGRES_URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from fastapi_users.db import SQLAlchemyUserDatabase
from typing import AsyncGenerator
from fastapi import Depends
from .models import User


DATABASE = f'postgresql+asyncpg://{POSTGRES_URL}'
ENGINE = create_async_engine(DATABASE)
SESSION = async_sessionmaker(ENGINE, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SESSION() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


if __name__ == '__main__':
    pass
