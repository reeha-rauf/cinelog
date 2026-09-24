from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date, CheckConstraint
from sqlalchemy.sql import func
from app.database import Base


class WatchLog(Base):
    __tablename__ = "watch_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    rating = Column(Integer, nullable=True)
    review = Column(Text, nullable=True)
    watched_on = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="rating_range"),
    )


class Watchlist(Base):
    __tablename__ = "watchlist"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    added_at = Column(DateTime, server_default=func.now())

