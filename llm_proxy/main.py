"""
Main entry point for the LLM Proxy module.
"""

import os
from .app import App

def main():
    """Main function for the LLM Proxy."""
    openai_token = os.environ.get("OPENAI_API_KEY")
    if not openai_token:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    app = App(openai_token)
    app.run()


# Export the web app for production use
def create_app():
    """Create and return the web application instance."""
    openai_token = os.environ.get("OPENAI_API_KEY")
    if not openai_token:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    app_instance = App(openai_token)
    return app_instance.web_app


if __name__ == "__main__":
    main() 