import os
from llm_proxy.app import App

openai_token = os.environ["OPENAI_API_KEY"]
oai_assistant_id = os.environ.get("OAI_ASSISTANT_ID")
app = App(openai_token, oai_assistant_id).web_app 