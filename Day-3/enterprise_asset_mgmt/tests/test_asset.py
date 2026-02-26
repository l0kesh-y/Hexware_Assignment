import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_it_admin_token():
    # Register IT Admin
    client.post("/auth/register", json={
        "name": "IT Admin",
        "email": "itadmin@company.com",
        "password": "admin123",
        "role": "IT_ADMIN"
    })
    
    # Login
    response = client.post("/auth/login", json={
        "email": "itadmin@company.com",
        "password": "admin123"
    })
    return response.json()["access_token"]

def test_create_asset():
    token = get_it_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/itadmin/assets", headers=headers, json={
        "asset_tag": "LAP002",
        "asset_type": "Laptop",
        "brand": "Dell",
        "model": "XPS 15"
    })
    assert response.status_code in [200, 201]
    assert response.json()["asset_tag"] == "LAP002"

def test_duplicate_asset_tag():
    token = get_it_admin_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create first asset
    client.post("/itadmin/assets", headers=headers, json={
        "asset_tag": "LAP003",
        "asset_type": "Laptop",
        "brand": "Dell",
        "model": "XPS 15"
    })
    
    # Try to create duplicate
    response = client.post("/itadmin/assets", headers=headers, json={
        "asset_tag": "LAP003",
        "asset_type": "Laptop",
        "brand": "HP",
        "model": "EliteBook"
    })
    assert response.status_code == 400
