def test_register_user_success(client):
    response = client.post("/auth/register", json={
    "username": "john",
    "email": "john@test.com",
    "password": "1234",
    "role": "candidate"
})

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"
    assert "id" in response.json()


def test_register_duplicate_email(client):
    # First registration
    client.post("/auth/register", json={
        "email": "john@test.com",
        "password": "1234",
        "role": "candidate"
    })

    # Duplicate registration
    response = client.post("/auth/register", json={
        "email": "john@test.com",
        "password": "1234",
        "role": "candidate"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success(client):
    # Register user
    client.post("/auth/register", json={
        "email": "mark@test.com",
        "password": "1234",
        "role": "candidate"
    })

    # Login
    response = client.post("/auth/login", json={
        "email": "mark@test.com",
        "password": "1234"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password(client):
    # Register user
    client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "1234",
        "role": "candidate"
    })

    # Wrong password
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"