from tests.conftest import signup_and_login


def test_add_to_watchlist(client):
    headers = signup_and_login(client, "watchlistuser")
    response = client.post("/logs/add/27205", headers=headers)
    assert response.status_code == 200


def test_add_to_watchlist_duplicate(client):
    headers = signup_and_login(client, "dupewatchlistuser")
    client.post("/logs/add/27205", headers=headers)
    response = client.post("/logs/add/27205", headers=headers)
    assert response.status_code == 400


def test_remove_from_watchlist(client):
    headers = signup_and_login(client, "removewatchlistuser")
    add_response = client.post("/logs/add/27205", headers=headers)
    movie_id = add_response.json()["movie_id"]

    response = client.delete(f"/logs/remove/{movie_id}", headers=headers)
    assert response.status_code == 204

    response = client.delete(f"/logs/remove/{movie_id}", headers=headers)
    assert response.status_code == 404


def test_list_watchlist(client):
    headers = signup_and_login(client, "listwatchlistuser")
    user_id = client.get("/auth/me", headers=headers).json()["id"]
    client.post("/logs/add/27205", headers=headers)

    response = client.get(f"/logs/watchlist/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1