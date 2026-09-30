def test_signup_success(client):
    response = client.post("/auth/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data

def test_signup_duplicate_username(client):
    client.post("/auth/signup", json={
        "username": "dupeuser",
        "email": "dupe1@example.com",
        "password": "testpass123"
    })
    response = client.post("/auth/signup", json={
        "username": "dupeuser",
        "email": "dupe2@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/signup", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "testpass123"
    })
    response = client.post("/auth/login", data={
        "username": "loginuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post("/auth/signup", json={
        "username": "wrongpassuser",
        "email": "wrongpass@example.com",
        "password": "testpass123"
    })
    response = client.post("/auth/login", data={
        "username": "wrongpassuser",
        "password": "incorrectpassword"
    })
    assert response.status_code == 401