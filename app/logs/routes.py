from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database import SessionLocal
from app.auth.models import User, Follow
from app.auth.routes import get_current_user
from app.movies.models import Movie
from app.movies.tmdb import get_movie_details, get_or_create_movie
from app.logs.models import WatchLog, Watchlist
from app.logs.schemas import WatchLogCreate, WatchLogResponse, WatchlistResponse, FeedEntry


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
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    db.refresh(log)
    return log


@router.get("/user/{user_id}", response_model=List[WatchLogResponse])
def get_user_logs(user_id: int, db: Session = Depends(get_db)):
    logs = db.query(WatchLog).filter(WatchLog.user_id == user_id).order_by(WatchLog.created_at.desc()).all()
    return logs


@router.post("/add/{tmdb_id}", response_model=WatchlistResponse)
async def add_to_watchlist(tmdb_id: int, user= Depends(get_current_user), db: Session = Depends(get_db)):
    try: 
        movie_data = await get_movie_details(tmdb_id)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to reach TMDB")
    
    movie = get_or_create_movie(db, movie_data)
    watchlist = Watchlist(user_id=user.id, movie_id=movie.id)
    db.add(watchlist)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Already on watchlist")
    
    db.refresh(watchlist)
    return watchlist

@router.delete("/remove/{movie_id}", status_code=204)
def remove_from_watchlist(movie_id:int, user = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(Watchlist).filter(
        Watchlist.user_id == user.id,
        Watchlist.movie_id == movie_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="This movie is not on your watchlist")
    db.delete(item)
    db.commit()


@router.get("/watchlist/{user_id}", response_model=List[WatchlistResponse])
def get_watchlist(user_id: int, db: Session = Depends(get_db)):
    watchlist = db.query(Watchlist).filter(Watchlist.user_id == user_id).order_by(Watchlist.added_at.desc()).all()
    return watchlist

@router.get("feed/", response_model=List[FeedEntry])
def get_feed(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    results = (
        db.query(WatchLog, User.username, Movie.title, Movie.poster_url)
        .join(User, WatchLog.user_id == User.id)
        .join(Movie, WatchLog.movie_id == Movie.id)
        .join(Follow, Follow.followed_id == WatchLog.user_id)
        .filter(Follow.follower_id == current_user.id)
        .order_by(WatchLog.created_at.desc())
        .limit(50)
        .all()
    )

    feed = []
    for log, username, title, poster in results:
        feed.append({
            "log_id": log.id,
            "username": username,
            "movie_title": title,
            "poster_url": poster,
            "rating": log.rating,
            "review": log.review,
            "watched_on": log.watched_on,
            "created_at": log.created_at,
        })

    return feed