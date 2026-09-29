from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.auth.models import User
from app.auth.routes import get_current_user
from app.movies.tmdb import get_movie_details, get_or_create_movie
from app.logs.models import WatchLog
from app.logs.schemas import WatchLogCreate, WatchLogResponse


router = APIRouter(prefix="/logs", tags=["logs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=WatchLogResponse)
async def create_log(log_data: WatchLogCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        movie_data = await get_movie_details(log_data.tmdb_id)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to reach TMDB")

    movie = get_or_create_movie(db, movie_data)

    log = WatchLog(
        user_id=current_user.id,
        movie_id=movie.id,
        rating=log_data.rating,
        review=log_data.review,
        watched_on=log_data.watched_on,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

