import pytest
from litestar.testing import TestClient
from src.user_api.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_user(client):
    response = client.post("/users", json={"name": "John", "surname": "Doe", "password": "secret"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John"
    assert "id" in data
    assert "created" in data