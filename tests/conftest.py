import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

load_dotenv()

from app.database import Base, get_db
from app.auth.models import User, Follow
from app.movies.models import Movie, Genre, MovieGenre
from app.logs.models import WatchLog, Watchlist
from main import app


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    with TestClient(app) as c:
        yield c

def signup_and_login(client, username="testuser", email=None):
    if email is None:
        email = f"{username}@example.com"
    client.post("/auth/signup", json={
        "username": username,
        "email": email,
        "password": "testpass123"
    })
    response = client.post("/auth/login", data={
        "username": username,
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}