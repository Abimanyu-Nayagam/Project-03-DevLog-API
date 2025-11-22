# tests/test_routes.py
import pytest
from app.models.db_models import db
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def snippet_data():
    return {
        "title": "Test Snippet",
        "language": "Python",
        "snippet": "print('hello world')",
        "description": "A test snippet",
        "tags": "test,python"
    }

@pytest.fixture
def entry_data():
    return {
        "title": "Test Entry",
        "content": "This is a test entry",
        "tags": "test,entry"
    }

# ------------------------
# CREATE ROUTES
# ------------------------
def test_create_snippet_success(auth_client, snippet_data):
    res = auth_client.post("/api/snippets", json=snippet_data)
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == snippet_data["title"]
    assert data["language"] == snippet_data["language"]

def test_create_snippet_missing_required(auth_client, snippet_data):
    for field in ["title", "language", "snippet", "description"]:
        bad_data = snippet_data.copy()
        bad_data.pop(field)
        res = auth_client.post("/api/snippets", json=bad_data)
        assert res.status_code == 400
        assert "error" in res.get_json()

def test_create_snippet_extra_field(auth_client, snippet_data):
    bad_data = snippet_data.copy()
    bad_data["extra"] = "not allowed"
    res = auth_client.post("/api/snippets", json=bad_data)
    assert res.status_code == 400

def test_create_snippet_wrong_type(auth_client, snippet_data):
    bad_data = snippet_data.copy()
    bad_data["title"] = 123  # Should be str
    res = auth_client.post("/api/snippets", json=bad_data)
    assert res.status_code == 400

def test_create_entry_success(auth_client, entry_data):
    res = auth_client.post("/api/entries", json=entry_data)
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == entry_data["title"]

def test_create_entry_missing_required(auth_client, entry_data):
    for field in ["title", "content"]:
        bad_data = entry_data.copy()
        bad_data.pop(field)
        res = auth_client.post("/api/entries", json=bad_data)
        assert res.status_code == 400

def test_create_entry_extra_field(auth_client, entry_data):
    bad_data = entry_data.copy()
    bad_data["extra"] = "not allowed"
    res = auth_client.post("/api/entries", json=bad_data)
    assert res.status_code == 400

def test_create_entry_wrong_type(auth_client, entry_data):
    bad_data = entry_data.copy()
    bad_data["title"] = 123
    res = auth_client.post("/api/entries", json=bad_data)
    assert res.status_code == 400

# ------------------------
# READ ROUTES
# ------------------------
def test_get_snippets_success(auth_client, snippet_data):
    auth_client.post("/api/snippets", json=snippet_data)
    res = auth_client.get("/api/snippets")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 1

def test_get_entries_success(auth_client, entry_data):
    auth_client.post("/api/entries", json=entry_data)
    res = auth_client.get("/api/entries")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 1

def test_get_snippet_by_invalid_id(auth_client):
    res = auth_client.get("/api/snippets/99999")
    assert res.status_code == 404

def test_get_entry_by_invalid_id(auth_client):
    res = auth_client.get("/api/entries/99999")
    assert res.status_code == 404

# ------------------------
# UPDATE ROUTES
# ------------------------
def test_update_snippet_success(auth_client, snippet_data):
    res = auth_client.post("/api/snippets", json=snippet_data)
    snippet_id = res.get_json()["id"]
    patch_data = {"id": snippet_id, "title": "Updated Snippet"}
    res2 = auth_client.patch("/api/snippets", json=patch_data)
    assert res2.status_code == 200
    assert res2.get_json()["title"] == "Updated Snippet"

def test_update_entry_success(auth_client, entry_data):
    res = auth_client.post("/api/entries", json=entry_data)
    entry_id = res.get_json()["id"]
    patch_data = {"id": entry_id, "title": "Updated Entry"}
    res2 = auth_client.patch("/api/entries", json=patch_data)
    assert res2.status_code == 200
    assert res2.get_json()["title"] == "Updated Entry"

def test_update_snippet_invalid(auth_client, snippet_data):
    res = auth_client.post("/api/snippets", json=snippet_data)
    snippet_id = res.get_json()["id"]
    bad_data = {"id": snippet_id, "extra": "not allowed"}
    res2 = auth_client.patch("/api/snippets", json=bad_data)
    assert res2.status_code == 400

def test_update_entry_invalid(auth_client, entry_data):
    res = auth_client.post("/api/entries", json=entry_data)
    entry_id = res.get_json()["id"]
    bad_data = {"id": entry_id, "extra": "not allowed"}
    res2 = auth_client.patch("/api/entries", json=bad_data)
    assert res2.status_code == 400

def test_update_nonexistent_snippet(auth_client):
    patch_data = {"id": 9999, "title": "Updated Snippet"}
    res = auth_client.patch("/api/snippets", json=patch_data)
    assert res.status_code == 404

def test_update_nonexistent_entry(auth_client):
    patch_data = {"id": 9999, "title": "Updated Entry"}
    res = auth_client.patch("/api/entries", json=patch_data)
    assert res.status_code == 404

# ------------------------
# DELETE ROUTES
# ------------------------
def test_delete_snippet_success(auth_client, snippet_data):
    res = auth_client.post("/api/snippets", json=snippet_data)
    snippet_id = res.get_json()["id"]
    res2 = auth_client.delete(f"/api/snippets/{snippet_id}")
    assert res2.status_code == 200
    res3 = auth_client.get(f"/api/snippets/{snippet_id}")
    assert res3.status_code == 404

def test_delete_entry_success(auth_client, entry_data):
    res = auth_client.post("/api/entries", json=entry_data)
    entry_id = res.get_json()["id"]
    res2 = auth_client.delete(f"/api/entries/{entry_id}")
    assert res2.status_code == 200
    res3 = auth_client.get(f"/api/entries/{entry_id}")
    assert res3.status_code == 404

def test_delete_nonexistent_snippet(auth_client):
    res = auth_client.delete("/api/snippets/9999")
    assert res.status_code == 404

def test_delete_nonexistent_entry(auth_client):
    res = auth_client.delete("/api/entries/9999")
    assert res.status_code == 404

# ------------------------
# SEARCH & FILTER
# ------------------------
def test_search_snippets_success(auth_client, snippet_data):
    auth_client.post("/api/snippets", json=snippet_data)
    res = auth_client.get("/api/snippets/search?q=Test")
    assert res.status_code == 200
    assert len(res.get_json()) >= 1

def test_search_snippets_no_query(auth_client):
    res = auth_client.get("/api/snippets/search")
    assert res.status_code == 400

def test_search_entries_success(auth_client, entry_data):
    auth_client.post("/api/entries", json=entry_data)
    res = auth_client.get("/api/entries/search?q=Test")
    assert res.status_code == 200
    assert len(res.get_json()) >= 1

def test_search_entries_no_query(auth_client):
    res = auth_client.get("/api/entries/search")
    assert res.status_code == 400

def test_filter_snippets_by_tag_success(auth_client, snippet_data):
    auth_client.post("/api/snippets", json=snippet_data)
    res = auth_client.get("/api/snippets/filter/tag/test")
    assert res.status_code == 200
    assert any("test" in s["tags"] for s in res.get_json())

def test_filter_snippets_by_tag_not_found(auth_client):
    res = auth_client.get("/api/snippets/filter/tag/nonexistent")
    assert res.status_code == 404

def test_filter_entries_by_tag_success(auth_client, entry_data):
    auth_client.post("/api/entries", json=entry_data)
    res = auth_client.get("/api/entries/filter/tag/test")
    assert res.status_code == 200

def test_filter_entries_by_tag_not_found(auth_client):
    res = auth_client.get("/api/entries/filter/tag/nonexistent")
    assert res.status_code == 404

def test_filter_snippets_by_language_success(auth_client, snippet_data):
    auth_client.post("/api/snippets", json=snippet_data)
    res = auth_client.get("/api/snippets/filter/language/Python")
    assert res.status_code == 200
    assert all(s["language"] == "Python" for s in res.get_json())

def test_filter_snippets_by_language_not_found(auth_client):
    res = auth_client.get("/api/snippets/filter/language/NonexistentLang")
    assert res.status_code == 404

def test_filter_entries_by_title_success(auth_client, entry_data):
    auth_client.post("/api/entries", json=entry_data)
    res = auth_client.get("/api/entries/filter/title/Test Entry")
    assert res.status_code == 200
    assert any(e["title"] == "Test Entry" for e in res.get_json())

def test_filter_entries_by_title_not_found(auth_client):
    res = auth_client.get("/api/entries/filter/title/NonexistentTitle")
    assert res.status_code == 404
