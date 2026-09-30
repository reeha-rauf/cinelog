from tests.conftest import signup_and_login


def test_follow_user(client):
    headers_a = signup_and_login(client, "followuser_a")
    headers_b = signup_and_login(client, "followuser_b")

    user_b_id = client.get("/auth/me", headers=headers_b).json()["id"]
    response = client.post(f"/auth/follow/{user_b_id}", headers=headers_a)
    assert response.status_code == 200


def test_follow_duplicate(client):
    headers_a = signup_and_login(client, "dupefollow_a")
    headers_b = signup_and_login(client, "dupefollow_b")

    user_b_id = client.get("/auth/me", headers=headers_b).json()["id"]
    client.post(f"/auth/follow/{user_b_id}", headers=headers_a)
    response = client.post(f"/auth/follow/{user_b_id}", headers=headers_a)
    assert response.status_code == 400


def test_follow_self(client):
    headers_a = signup_and_login(client, "selffollow_a")
    user_a_id = client.get("/auth/me", headers=headers_a).json()["id"]

    response = client.post(f"/auth/follow/{user_a_id}", headers=headers_a)
    assert response.status_code == 400


def test_follow_nonexistent_user(client):
    headers_a = signup_and_login(client, "ghostfollow_a")
    response = client.post("/auth/follow/999999", headers=headers_a)
    assert response.status_code == 404


def test_unfollow_user(client):
    headers_a = signup_and_login(client, "unfollow_a")
    headers_b = signup_and_login(client, "unfollow_b")

    user_b_id = client.get("/auth/me", headers=headers_b).json()["id"]
    client.post(f"/auth/follow/{user_b_id}", headers=headers_a)

    response = client.delete(f"/auth/unfollow/{user_b_id}", headers=headers_a)
    assert response.status_code == 204

    response = client.delete(f"/auth/unfollow/{user_b_id}", headers=headers_a)
    assert response.status_code == 404


def test_followers_and_following_lists(client):
    headers_a = signup_and_login(client, "listfollow_a")
    headers_b = signup_and_login(client, "listfollow_b")

    user_a_id = client.get("/auth/me", headers=headers_a).json()["id"]
    user_b_id = client.get("/auth/me", headers=headers_b).json()["id"]

    client.post(f"/auth/follow/{user_b_id}", headers=headers_a)

    followers = client.get(f"/auth/followers/{user_b_id}").json()
    assert any(f["id"] == user_a_id for f in followers)

    following = client.get(f"/auth/following/{user_a_id}").json()
    assert any(f["id"] == user_b_id for f in following)