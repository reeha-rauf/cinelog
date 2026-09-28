from pydantic import BaseModel

class MovieResponse(BaseModel):
    id: int
    tmdb_id: int
    title: str
    release_year: int | None
    poster_url: str | None
    overview: str | None
    director: str | None

    class Config:
        from_attributes = True

        