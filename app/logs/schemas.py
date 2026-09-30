from pydantic import BaseModel
from datetime import date, datetime

class WatchLogCreate(BaseModel):
    tmdb_id: int
    rating: int | None = None
    review: str | None = None
    watched_on: date | None = None


class WatchLogResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    rating: int | None
    review: str | None
    watched_on: date | None
    created_at: datetime

    class Config:
        from_attributes = True


class WatchlistResponse(BaseModel):
    user_id: int
    movie_id: int

    class Config:
        from_attributes = True


class FeedEntry(BaseModel):
    log_id: int
    username: str
    movie_title: str
    poster_url: str | None
    rating: int | None
    review: str | None
    watched_on: date | None
    created_at: datetime
