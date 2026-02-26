import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role": "EMPLOYEE"
    })
    assert response.status_code == 200
    assert "email" in response.json()

def test_login_user():
    # First register
    client.post("/auth/register", json={
        "name": "Login Test",
        "email": "login@example.com",
        "password": "password123",
        "role": "EMPLOYEE"
    })
    
    # Then login
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login():
    response = client.post("/auth/login", json={
        "email": "invalid@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
