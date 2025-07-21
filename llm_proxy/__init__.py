"""
LLM Proxy Module
"""

__version__ = "0.1.0"
from llm_proxy.app import App
import os

def create_app():
    """Factory to create FastAPI app for testing or running."""
    openai_token = os.environ.get("OPENAI_API_KEY", "")
    oai_assistant_id = os.environ.get("OAI_ASSISTANT_ID")
    app = App(openai_token, oai_assistant_id)
    return app.web_app 