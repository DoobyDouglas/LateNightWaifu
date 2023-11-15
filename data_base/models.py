from sqlalchemy import ForeignKey
from sqlalchemy import (
    String,
    Integer,
    Float,
    CheckConstraint,
    UniqueConstraint,
    Date,
    Text,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable


class Base(DeclarativeBase):
    pass


class Anime_Genre(Base):

    __tablename__ = 'Anime_Genre'

    anime_id = mapped_column(ForeignKey('Anime.id'), primary_key=True)
    genre_id = mapped_column(ForeignKey('Genre.id'), primary_key=True)


class Profile_Anime_Rating(Base):

    __tablename__ = 'Profile_Anime_Rating'

    anime_id = mapped_column(ForeignKey('Anime.id'), primary_key=True)
    profile_id = mapped_column(ForeignKey('Profile.id'), primary_key=True)
    rating = mapped_column(Integer)


class Anime(Base):

    __tablename__ = 'Anime'

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(255))
    director_id = mapped_column(ForeignKey('Director.id'))
    director = relationship('Director', back_populates='anime_list')
    genres = relationship(
        'Genre', Anime_Genre.__table__, back_populates='anime_list'
    )
    description = mapped_column(Text)
    release_date = mapped_column(Date, nullable=False)
    rating = mapped_column(
        Float, CheckConstraint('rating >= 0 and rating <= 10'), default=0
    )
    rating_count = mapped_column(Integer, default=0)
    rate_by = relationship(
        'Profile', Profile_Anime_Rating.__table__, back_populates='rated_anime'
    )
    poster = mapped_column(String(255), nullable=True)
    trailer = mapped_column(String(255), nullable=True)
    author_id = mapped_column(ForeignKey('Profile.id'))
    author = relationship('Profile', back_populates='posts')

    __table_args__ = (
        UniqueConstraint(
            'title', 'director_id', 'release_date', name='anime_director'
        ),
    )


class Director(Base):

    __tablename__ = 'Director'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), unique=True)
    anime_list = relationship('Anime', back_populates='director')


class Genre(Base):

    __tablename__ = 'Genre'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), unique=True)
    anime_list = relationship(
        'Anime', Anime_Genre.__table__, back_populates='genres'
    )


class User(SQLAlchemyBaseUserTable[int], Base):

    __tablename__ = 'User'

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(255))
    email = mapped_column(String(255), unique=True)
    hashed_password = mapped_column(String(255))
    profile = relationship('Profile', uselist=False, back_populates='user')


class Profile(Base):

    __tablename__ = 'Profile'

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('User.id'), unique=True)
    user = relationship('User', back_populates='profile')
    rated_anime = relationship(
        'Anime', Profile_Anime_Rating.__table__, back_populates='rate_by'
    )
    posts = relationship('Anime', back_populates='author')
    contribution = mapped_column(
        Float, CheckConstraint('rating >= 0'), default=0
    )

    __table_args__ = (UniqueConstraint('user_id'),)
