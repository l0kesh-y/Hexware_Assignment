import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_user():
    response = client.post("/auth/register", json={
        "name": "Test Employee",
        "email": "employee@company.com",
        "password": "emp123",
        "role": "EMPLOYEE"
    })
    assert response.status_code in [200, 201, 400]  # 400 if already exists

def test_login_user():
    # Register first
    client.post("/auth/register", json={
        "name": "Login Test",
        "email": "logintest@company.com",
        "password": "test123",
        "role": "EMPLOYEE"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "email": "logintest@company.com",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_login():
    response = client.post("/auth/login", json={
        "email": "invalid@company.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
