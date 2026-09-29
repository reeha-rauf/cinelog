from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.movies.tmdb import search_movies, get_movie_details, get_or_create_movie


router = APIRouter(prefix="/movies", tags=["movies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search")
async def search(query: str):
    try:
        data = await search_movies(query)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to reach TMDB")
    return data["results"]

@router.get("/{tmdb_id}")
async def get_movie(tmdb_id: int, db: Session = Depends(get_db)):
    try:
        data = await get_movie_details(tmdb_id)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed tp reach TMDB")
    movie = get_or_create_movie(db, data)
    return data

