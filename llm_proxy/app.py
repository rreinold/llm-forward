"""
App module for the LLM Proxy.
"""

import asyncio
import httpx
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware

BASE_OPENAI_URL = "https://api.openai.com"

logger = logging.getLogger(__name__)

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
    
    def __init__(self, openai_token: str, oai_assistant_id: str = None):
        """Initialize the app with OpenAI token and optional assistant ID."""
        self.name = "LLM Proxy"
        self.openai_token = openai_token
        self.oai_assistant_id = oai_assistant_id
        self.forward_url = f"/v1/assistants/{self.oai_assistant_id}/messages" if self.oai_assistant_id else "/v1/chat/completions"
        self.web_app = FastAPI(title="LLM Proxy")
        # --- Add CORS middleware ---
        self.web_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # You can restrict this to specific domains
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        # --- End CORS middleware addition ---
        self._setup_routes(self.forward_url)
    
    async def _chat_with_openai(self, request: ChatRequest):
        url = f"{BASE_OPENAI_URL}{self.forward_url}"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
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

    async def _chat_with_assistant(self, request: ChatRequest):
        assistant_headers = {
            "Authorization": f"Bearer {self.openai_token}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        # 1. Create a thread
        thread_resp = await httpx.AsyncClient().post(
            f"{BASE_OPENAI_URL}/v1/threads",
            headers=assistant_headers,
            json={}
        )
        thread_resp.raise_for_status()
        thread_id = thread_resp.json()["id"]

        # 2. Add a message to the thread
        last_msg = request.messages[-1]
        if isinstance(last_msg, dict):
            user_message = last_msg.get("content")
        else:
            user_message = getattr(last_msg, "content", str(last_msg))
        msg_payload = {
            "role": "user",
            "content": user_message
        }
        msg_resp = await httpx.AsyncClient().post(
            f"{BASE_OPENAI_URL}/v1/threads/{thread_id}/messages",
            headers=assistant_headers,
            json=msg_payload
        )
        msg_resp.raise_for_status()

        # 3. Run the assistant
        run_resp = await httpx.AsyncClient().post(
            f"{BASE_OPENAI_URL}/v1/threads/{thread_id}/runs",
            headers=assistant_headers,
            json={"assistant_id": self.oai_assistant_id}
        )
        run_resp.raise_for_status()
        run_id = run_resp.json()["id"]

        # 4. Poll for run completion
        for _ in range(180):
            run_status_resp = await httpx.AsyncClient().get(
                f"{BASE_OPENAI_URL}/v1/threads/{thread_id}/runs/{run_id}",
                headers=assistant_headers
            )
            run_status_resp.raise_for_status()
            status = run_status_resp.json()["status"]
            if status == "completed":
                break
            await asyncio.sleep(1)
        else:
            raise HTTPException(status_code=504, detail="Assistant run did not complete in time.")

        # 5. Retrieve the assistant's response
        messages_resp = await httpx.AsyncClient().get(
            f"{BASE_OPENAI_URL}/v1/threads/{thread_id}/messages",
            headers=assistant_headers
        )
        messages_resp.raise_for_status()
        messages = messages_resp.json()["data"]
        # Find the latest assistant message
        assistant_message = next((m for m in messages if m["role"] == "assistant"), None)
        if not assistant_message:
            raise HTTPException(status_code=500, detail="No assistant response found.")
        return {"assistant_response": assistant_message["content"]}

    def _setup_routes(self, forward_url: str):
        """Setup FastAPI routes."""
        @self.web_app.post(forward_url)
        async def chat_completions(request: ChatRequest):
            try:
                if self.oai_assistant_id:
                    return await self._chat_with_assistant(request)
                else:
                    return await self._chat_with_openai(request)
            except httpx.RequestError as e:
                logger.exception()
                raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
            except httpx.HTTPStatusError as e:
                logger.exception()
                raise HTTPException(status_code=e.response.status_code, detail=f"OpenAI API error: {e.response.text}")
    

    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the web application (for development)."""
        import uvicorn
        print(f"Running {self.name} with OpenAI token: {self.openai_token[:10]}...")
        print(f"Server starting on http://{host}:{port}")
        uvicorn.run(self.web_app, host=host, port=port) 