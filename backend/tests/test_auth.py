import json
from app.models.db_models import User, db

# -----------------------
# REGISTER TESTS
# -----------------------

def test_register_missing_email(client):
    res = client.post("/register", json={
        "username": "abc",
        "password": "123"
    })
    assert res.status_code == 400
    assert "Email is required" in res.get_json()["error"]


def test_register_missing_username(client):
    res = client.post("/register", json={
        "email": "test@example.com",
        "password": "123"
    })
    assert res.status_code == 400
    assert "Username is required" in res.get_json()["error"]


def test_register_missing_password(client):
    res = client.post("/register", json={
        "email": "test@example.com",
        "username": "abc",
    })
    assert res.status_code == 400
    assert "Password is required" in res.get_json()["error"]


def test_register_success(client):
    res = client.post("/register", json={
        "email": "test@example.com",
        "username": "abc",
        "password": "1234"
    })

    assert res.status_code == 201
    data = res.get_json()
    assert "registered successfully" in data["message"]

    # Ensure the user is in the DB
    with client.application.app_context():
        user = User.query.filter_by(username="abc").first()
        assert user is not None
        assert user.email == "test@example.com"


def test_register_duplicate_user(client):
    client.post("/register", json={
        "email": "dup@example.com",
        "username": "duplicate",
        "password": "pass"
    })

    # try again → should fail
    res = client.post("/register", json={
        "email": "dup@example.com",
        "username": "duplicate",
        "password": "pass"
    })

    assert res.status_code == 409
    assert "already exists" in res.get_json()["error"]


# -----------------------
# LOGIN TESTS
# -----------------------

def test_login_missing_username(client):
    res = client.post("/login", json={
        "password": "123"
    })
    assert res.status_code == 400
    assert "Username is required" in res.get_json()["error"]


def test_login_missing_password(client):
    res = client.post("/login", json={
        "username": "abc"
    })
    assert res.status_code == 400
    assert "Password is required" in res.get_json()["error"]


def test_login_nonexistent_user(client):
    res = client.post("/login", json={
        "username": "ghost",
        "password": "pass"
    })
    assert res.status_code == 401
    assert "does not exist" in res.get_json()["error"]


def test_login_success(client):
    # First register a user
    client.post("/register", json={
        "email": "testlogin@example.com",
        "username": "loginuser",
        "password": "mypassword"
    })
    # Now login
    res = client.post("/login", json={
        "username": "loginuser",
        "password": "mypassword"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data