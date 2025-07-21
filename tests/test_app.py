"""
Integration tests for LLM Proxy.

These tests call the actual OpenAI API and require a valid API key.
"""

import os
import pytest
from llm_proxy.main import create_app


@pytest.mark.integration
class TestLLMProxyIntegration:
    """Integration tests for LLM Proxy endpoints."""
    
    @pytest.fixture
    def app(self):
        """Create test app instance."""
        return create_app()
    
    @pytest.fixture
    def client(self, app):
        """Create test client."""
        from fastapi.testclient import TestClient
        return TestClient(app)
    
    def test_chat_completion_endpoint(self, client):
        """Test the chat completion endpoint with real OpenAI call."""
        assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not set"
        
        # Test data
        test_data = {
            "messages": [
                {"role": "user", "content": "Say hello in one word"}
            ],
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 10
        }
        
        # Make request to our proxy
        response = client.post("/v1/chat/completions", json=test_data)
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "choices" in data
        assert len(data["choices"]) > 0
        assert "message" in data["choices"][0]
        assert "content" in data["choices"][0]["message"]
        
        # Check that we got a response
        content = data["choices"][0]["message"]["content"]
        assert len(content) > 0
        assert isinstance(content, str)
        
        print(f"OpenAI response: {content}")
    
    def test_chat_completion_with_system_message(self, client):
        """Test chat completion with system message."""
        assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not set"
        
        test_data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that responds with short answers."},
                {"role": "user", "content": "What is 2+2?"}
            ],
            "model": "gpt-3.5-turbo",
            "temperature": 0.1,
            "max_tokens": 20
        }
        
        response = client.post("/v1/chat/completions", json=test_data)
        
        assert response.status_code == 200
        data = response.json()
        
        content = data["choices"][0]["message"]["content"]
        assert "4" in content or "four" in content.lower()
        
        print(f"Math response: {content}")
    
    def test_invalid_api_key(self):
        """Test behavior with invalid API key."""
        # Temporarily set invalid key
        original_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "invalid-key"
        
        try:
            from llm_proxy.app import App
            from fastapi.testclient import TestClient
            
            app_instance = App("invalid-key")
            client = TestClient(app_instance.web_app)
            
            test_data = {
                "messages": [{"role": "user", "content": "Hello"}],
                "model": "gpt-3.5-turbo"
            }
            
            response = client.post("/v1/chat/completions", json=test_data)
            
            # Should get 401 or 400 from OpenAI
            assert response.status_code in [400, 401, 403, 500]
            
        finally:
            # Restore original key
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
            else:
                del os.environ["OPENAI_API_KEY"]
    
    def test_missing_messages(self, client):
        """Test validation of missing messages."""
        test_data = {
            "model": "gpt-3.5-turbo"
        }
        
        response = client.post("/v1/chat/completions", json=test_data)
        
        # Should get validation error
        assert response.status_code == 422
    
    def test_empty_messages(self, client):
        """Test validation of empty messages."""
        test_data = {
            "messages": [],
            "model": "gpt-3.5-turbo"
        }
        
        response = client.post("/v1/chat/completions", json=test_data)
        
        # Should get validation error (400 or 422)
        assert response.status_code in [400, 422] 