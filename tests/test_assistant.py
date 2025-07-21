"""
Integration test for LLM Proxy with a specific assistant ID.
"""

import os
import pytest
from llm_proxy.app import App
from fastapi.testclient import TestClient

ASSISTANT_ID = "asst_JF0fe2OdKnFHicJGqQ68RNbt"

@pytest.mark.integration
def test_assistant_recipe_query():
    """Test chat completion with assistant ID, asking about recipes."""
    openai_token = os.environ.get("OPENAI_API_KEY", "")
    app = App(openai_token, ASSISTANT_ID).web_app
    client = TestClient(app)

    test_data = {
        "messages": [
            {"role": "user", "content": "Can you suggest a recipe for dinner?"}
        ],
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 100
    }

    response = client.post(f"/v1/assistants/{ASSISTANT_ID}/messages", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "assistant_response" in data
    content = data["assistant_response"][0]["text"]["value"]
    assert "recipe" in content.lower() or "ingredients" in content.lower() or len(content) > 0 