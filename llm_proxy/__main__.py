"""
Entry point for running the LLM proxy as a module.
"""

import os
from llm_proxy.app import App

if __name__ == "__main__":
    openai_token = os.environ.get("OPENAI_API_KEY", "")
    oai_assistant_id = os.environ.get("OAI_ASSISTANT_ID")
    app = App(openai_token, oai_assistant_id)
    app.run() 