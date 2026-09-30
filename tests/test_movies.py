def test_search_movies(client):
    response = client.get("/movies/search", params={"query": "Inception"})
    assert response.status_code == 200
    results = response.json()
    assert any(movie["title"] == "Inception" for movie in results)


def test_get_movie_detail_caches_movie(client, db_session):
    from app.movies.models import Movie

    response = client.get("/movies/27205")
    assert response.status_code == 200
    assert response.json()["title"] == "Inception"

    cached = db_session.query(Movie).filter(Movie.tmdb_id == 27205).first()
    assert cached is not None
    assert cached.title == "Inception"