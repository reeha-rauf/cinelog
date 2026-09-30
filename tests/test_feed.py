from tests.conftest import signup_and_login


def test_feed_shows_followed_users_logs(client):
    headers_a = signup_and_login(client, "feeduser_a")
    headers_b = signup_and_login(client, "feeduser_b")

    user_b_id = client.get("/auth/me", headers=headers_b).json()["id"]
    client.post(f"/auth/follow/{user_b_id}", headers=headers_a)

    client.post("/logs/", json={
        "tmdb_id": 27205,
        "rating": 5,
        "review": "From user B",
        "watched_on": "2026-09-30"
    }, headers=headers_b)

    response = client.get("/logs/feed", headers=headers_a)
    assert response.status_code == 200
    feed = response.json()
    assert any(entry["username"] == "feeduser_b" for entry in feed)


def test_feed_empty_when_not_following_anyone(client):
    headers = signup_and_login(client, "lonelyfeeduser")
    response = client.get("/logs/feed", headers=headers)
    assert response.status_code == 200
    assert response.json() == []