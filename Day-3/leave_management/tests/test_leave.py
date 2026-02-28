import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta

client = TestClient(app)

def get_auth_token():
    # Register and login
    client.post("/auth/register", json={
        "name": "Employee Test",
        "email": "employee@example.com",
        "password": "password123",
        "role": "EMPLOYEE",
        "department_id": 1
    })
    
    response = client.post("/auth/login", json={
        "email": "employee@example.com",
        "password": "password123"
    })
    return response.json()["access_token"]

def test_apply_leave():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    today = date.today()
    response = client.post("/employee/leaves", headers=headers, json={
        "start_date": str(today + timedelta(days=1)),
        "end_date": str(today + timedelta(days=3)),
        "reason": "Vacation"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"

def test_unauthorized_access():
    response = client.get("/employee/leaves")
    assert response.status_code == 401
