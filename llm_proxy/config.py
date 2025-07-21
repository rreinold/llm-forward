from pydantic import BaseSettings, Field
from typing import Optional

class LLMProxySettings(BaseSettings):
    """Settings for LLM Proxy loaded from environment variables."""
    openai_api_key: str = Field(..., env="OPENAI_API_KEY", description="Your OpenAI API key (required).")
    public_access_key: Optional[str] = Field(None, env="LLM_PROXY_PUBLIC_ACCESS_KEY", description="Optional public access key for proxy authentication.")
    oai_assistant_id: Optional[str] = Field(None, env="OAI_ASSISTANT_ID", description="Optional OpenAI Assistant ID for routing requests.")
    port: int = Field(8000, env="LLM_PROXY_PORT", description="Port for running the proxy server.")

    # Optional .env
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings: Optional[LLMProxySettings] = None

def get_settings() -> LLMProxySettings:
    global settings
    if not settings:
        settings = LLMProxySettings()
    return settings 