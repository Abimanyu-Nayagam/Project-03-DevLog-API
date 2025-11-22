# tests/conftest.py
import pytest
from app import create_app
from app.models.db_models import db
from config.config import TestConfig

@pytest.fixture
def test_app():
    # Override config for tests
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()  # creates test tables
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

@pytest.fixture
def auth_client(test_app):
    client = test_app.test_client()

    # Register a user
    client.post("/api/register", json={
        "email": "testauth@example.com",
        "username": "authuser",
        "password": "password123"
    })

    # Login to get access token
    res = client.post("/api/login", json={
        "username": "authuser",
        "password": "password123"
    })

    token = res.get_json()["access_token"]

    # Attach token to headers automatically
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    return client
