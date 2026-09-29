import os
import httpx
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.movies.models import Movie, Genre, MovieGenre


load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

async def search_movies(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TMDB_BASE_URL}/search/movie",
            params={"api_key": TMDB_API_KEY, "query": query}
        )
        response.raise_for_status()
        return response.json()

def get_or_create_movie(db: Session, tmdb_movie: dict) -> Movie:
    existing = db.query(Movie).filter(Movie.tmdb_id == tmdb_movie["id"]).first()
    if existing:
        return existing

    release_date = tmdb_movie.get("release_date") or ""
    release_year = int(release_date[:4]) if release_date else None

    director = None
    for crew_member in tmdb_movie.get("credits", {}).get("crew", []):
        if crew_member.get("job") == "Director":
            director = crew_member["name"]
            break

    movie = Movie(
        tmdb_id=tmdb_movie["id"],
        title=tmdb_movie["title"],
        release_year=release_year,
        poster_url=tmdb_movie.get("poster_path"),
        overview=tmdb_movie.get("overview"),
        director=director,
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)

    for genre_data in tmdb_movie.get("genres", []):
        genre = get_or_create_genre(db, genre_data["name"])
        db.add(MovieGenre(movie_id=movie.id, genre_id=genre.id))
    db.commit()

    return movie

def get_or_create_genre(db: Session, genre_name: str) -> Genre:
    existing = db.query(Genre).filter(Genre.name == genre_name).first()
    if existing:
        return existing
    genre = Genre(name=genre_name)
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre


async def get_movie_details(tmdb_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TMDB_BASE_URL}/movie/{tmdb_id}",
            params={"api_key": TMDB_API_KEY, "append_to_response": "credits"}
        )
        response.raise_for_status()
        return response.json()

