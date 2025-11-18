import json
from app import db
from io import BytesIO

# Helpers
def register_and_login(client):
    # Register
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    # Login
    login_res = client.post("/login", json={
        "username": "testuser",
        "password": "password123"
    })

    token = login_res.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_entry(client, headers):
    res = client.post("/api/v1/entries", json={
        "title": "My Entry",
        "content": "This is a test entry",
        "tags": "test"
    }, headers=headers)

    assert res.status_code == 201
    return res.get_json()["id"]


def create_snippet(client, headers):
    res = client.post("/api/v1/snippets", json={
        "title": "Snippet One",
        "snippet": "print('hello')",
        "language": "python",
        "tags": "test",
        "description": "desc"
    }, headers=headers)

    assert res.status_code == 201
    return res.get_json()["id"]


# -------------------------------
# EXPORT ENTRY AS MD
# -------------------------------
def test_export_entry_md(client):
    headers = register_and_login(client)
    entry_id = create_entry(client, headers)

    res = client.get(f"/export-entry-md/v1/{entry_id}", headers=headers)
    assert res.status_code == 200
    assert res.mimetype == "text/markdown"


# -------------------------------
# EXPORT SNIPPET AS MD
# -------------------------------
def test_export_snippet_md(client):
    headers = register_and_login(client)
    snippet_id = create_snippet(client, headers)

    res = client.get(f"/export-snippet-md/v1/{snippet_id}", headers=headers)
    assert res.status_code == 200
    assert res.mimetype == "text/markdown"


# -------------------------------
# EXPORT SNIPPET AS JSON
# -------------------------------
def test_export_snippet_json(client):
    headers = register_and_login(client)
    snippet_id = create_snippet(client, headers)

    res = client.get(f"/export-snippet-json/v1/{snippet_id}", headers=headers)
    assert res.status_code == 200
    assert res.mimetype == "application/json"


# -------------------------------
# EXPORT ENTRY AS JSON
# -------------------------------
def test_export_entry_json(client):
    headers = register_and_login(client)
    entry_id = create_entry(client, headers)

    res = client.get(f"/export-entry-json/v1/{entry_id}", headers=headers)
    assert res.status_code == 200
    assert res.mimetype == "application/json"
