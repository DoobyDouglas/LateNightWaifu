from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float, CheckConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy.orm import mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable


class Base(DeclarativeBase):
    pass


# Anime_Genre = Table(
#     'Anime_Genre',
#     Base.metadata,
#     Column('anime_id', ForeignKey('Anime.id'), primary_key=True),
#     Column('genre_id', ForeignKey('Genre.id'), primary_key=True),
# )

class Anime_Genre(Base):

    __tablename__ = 'Anime_Genre'

    anime_id = mapped_column(ForeignKey('Anime.id'), primary_key=True)
    genre_id = mapped_column(ForeignKey('Genre.id'), primary_key=True)


class User_Anime_Rating(Base):

    __tablename__ = 'User_Anime_Rating'

    anime_id = mapped_column(ForeignKey('Anime.id'), primary_key=True)
    user_id = mapped_column(ForeignKey('User.id'), primary_key=True)
    rating = mapped_column(Integer)


class Anime(Base):

    __tablename__ = 'Anime'

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(255))
    director_id = mapped_column(ForeignKey('Director.id'))
    director = relationship('Director', back_populates='anime_list')
    genres = relationship('Genre', Anime_Genre.__table__, back_populates='anime_list')
    rating = mapped_column(
        Float, CheckConstraint('rating >= 0 and rating <= 10')
    )
    rating_count = mapped_column(Integer)
    rate_by = relationship('User', User_Anime_Rating.__table__, back_populates='rated_anime')


class Director(Base):

    __tablename__ = 'Director'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    anime_list = relationship('Anime', back_populates='director')


class Genre(Base):

    __tablename__ = 'Genre'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    anime_list = relationship('Anime', Anime_Genre.__table__, back_populates='genres')


class User(SQLAlchemyBaseUserTable[int], Base):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email: Column(String(255))
    hashed_password: Column(String(255))
    rated_anime = relationship(
        'Anime', User_Anime_Rating.__table__, back_populates='rate_by'
    )
