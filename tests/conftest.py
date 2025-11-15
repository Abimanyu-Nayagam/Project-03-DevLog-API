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
