import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../app"))
from app.main import app
import pytest
from fastapi.testclient import TestClient


client = TestClient(app)

# Test login endpoint
def test_login_success():
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test protected endpoint with valid JWT
def test_access_protected_with_valid_jwt():
    login_response = client.post("/auth/login", json={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    protected_response = client.get("/protected", headers=headers)
    assert protected_response.status_code == 200

# Test protected endpoint with invalid JWT
def test_access_protected_with_invalid_jwt():
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401

# Test protected endpoint with expired JWT (simulate if possible)
def test_access_protected_with_expired_jwt():
    # This test assumes you can generate an expired token or mock the validation
    expired_token = "expired.jwt.token"
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
