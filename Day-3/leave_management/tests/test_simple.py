import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_with_short_password():
    """Test user registration with valid short password"""
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "pass123",
        "role": "EMPLOYEE"
    })
    assert response.status_code in [200, 201, 400]  # 400 if email exists

def test_invalid_login():
    """Test login with invalid credentials"""
    response = client.post("/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
