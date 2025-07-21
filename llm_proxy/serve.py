import os
from llm_proxy.app import App
from llm_proxy.config import get_settings

settings = get_settings()
app = App(settings.openai_api_key, settings.oai_assistant_id).web_app 