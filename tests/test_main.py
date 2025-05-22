from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_create_account_and_login():
    # Create user
    user_data = {"username": "testuser", "email": "test@example.com", "password": "testpass"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 200
    assert res.json()["username"] == "testuser"

    # Login user
    login_data = {"username": "testuser", "password": "testpass"}
    res = client.post("/login/", data=login_data)
    assert res.status_code == 200
    assert res.json()["username"] == "testuser"
