from fastapi import APIRouter, HTTPException
from app.movies.tmdb import search_movies, get_movie_details


router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/search")
async def search(query: str):
    try:
        data = await search_movies(query)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to reach TMDB")
    return data["results"]

@router.get("/{tmdb_id}")
async def get_movie(tmdb_id: int):
    try:
        data = await get_movie_details(tmdb_id)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed tp reach TMDB")
    return data