from tests.conftest import signup_and_login


def test_create_log(client):
    headers = signup_and_login(client, "loguser")
    response = client.post("/logs/", json={
        "tmdb_id": 27205,
        "rating": 5,
        "review": "Great movie",
        "watched_on": "2026-09-30"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["rating"] == 5


def test_create_log_invalid_rating(client):
    headers = signup_and_login(client, "badratinguser")
    response = client.post("/logs/", json={
        "tmdb_id": 27205,
        "rating": 10,
        "review": "test",
        "watched_on": "2026-09-30"
    }, headers=headers)
    assert response.status_code == 400


def test_list_user_logs(client):
    headers = signup_and_login(client, "listloguser")
    user_id = client.get("/auth/me", headers=headers).json()["id"]

    client.post("/logs/", json={
        "tmdb_id": 27205,
        "rating": 4,
        "review": "Rewatch",
        "watched_on": "2026-09-30"
    }, headers=headers)

    response = client.get(f"/logs/user/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1