# tests/test_autogen_routes.py
import pytest
from unittest.mock import patch

@pytest.mark.parametrize("route, key", [
    ("/api/autogen/title", "title"),
    ("/api/autogen/description", "description"),
    ("/api/autogen/tags", "tags")
])
def test_autogen_routes(auth_client, route, key):
    """
    Test all /autogen routes with mocked Gemini API.
    """
    # Sample input payload
    payload = {
        "content": "def add(a, b): return a + b",
        "language": "python",
        "title": "Add Function"
    }

    # Expected mocked response text
    mock_response_text = f"mocked {key}"

    # Patch the model.generate_content method
    with patch("app.routes.autogen_route.genai.GenerativeModel") as MockModel:
        instance = MockModel.return_value
        instance.generate_content.return_value.text = mock_response_text

        # Make POST request
        res = auth_client.post(route, json=payload)

        # Check status code
        assert res.status_code == 200

        # Check response contains the expected key and value
        json_data = res.get_json()
        assert key in json_data
        assert json_data[key] == mock_response_text
