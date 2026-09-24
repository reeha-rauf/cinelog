from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    release_year = Column(Integer, nullable=True)
    poster_url = Column(String(500), nullable=True)
    overview = Column(Text, nullable=True)
    director = Column(String(255), nullable=True)
    cached_at = Column(DateTime, server_default=func.now())


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

class MovieGenre(Base):
    __tablename__ = "movie_genres"

    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)

    