"""
App module for the LLM Proxy.
"""

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000

class App:
    """Main application class for LLM Proxy."""
    
    def __init__(self, openai_token: str):
        """Initialize the app with OpenAI token."""
        self.name = "LLM Proxy"
        self.openai_token = openai_token
        self.web_app = FastAPI(title="LLM Proxy")
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup FastAPI routes."""
        
        @self.web_app.post("/v1/chat/completions")
        async def chat_completions(request: ChatRequest):
            """Reroute chat completion requests to OpenAI."""
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openai_token}",
                            "Content-Type": "application/json"
                        },
                        json=request.model_dump()
                    )
                    
                    if response.status_code != 200:
                        raise HTTPException(
                            status_code=response.status_code,
                            detail=f"OpenAI API error: {response.text}"
                        )
                    
                    return response.json()
                    
            except httpx.RequestError as e:
                raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    

    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the web application (for development)."""
        import uvicorn
        print(f"Running {self.name} with OpenAI token: {self.openai_token[:10]}...")
        print(f"Server starting on http://{host}:{port}")
        uvicorn.run(self.web_app, host=host, port=port) 