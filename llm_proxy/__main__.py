"""
Entry point for running the LLM proxy as a module.
"""

import os
import uvicorn
from .main import create_app
from .exceptions import LLMForwardConfigError

def main():
    """Run the LLM proxy server."""
    # Check for required environment variable
    if not os.environ.get("OPENAI_API_KEY"):
        raise LLMForwardConfigError("OPENAI_API_KEY environment variable not set. Please set your OpenAI API key.")
    
    # Create the FastAPI app
    app = create_app()
    
    # Run with uvicorn
    print("Starting LLM Proxy server in development mode...")
    print(f"OpenAI API Key: {os.environ.get('OPENAI_API_KEY')[:10]}...")
    print("Server will be available at http://localhost:8000")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main() 