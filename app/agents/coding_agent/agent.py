import os
from langchain.chat_models import init_chat_model
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.agents import create_agent

from app.agents.tools.execute_code import execute_code
from app.agents.tools.read_write_file import read_file, write_file
from app.agents.utils.load_yaml_prompts import load_prompt
from app.core.config import get_settings

settings = get_settings()
PROMPT_FILE = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'coding_agent_prompt.yaml')

os.makedirs(settings.WORK_DIR, exist_ok=True)

basic_model = init_chat_model(
    settings.CODING_AGENT_BASIC_MODEL,
    model_provider='google_genai',
    api_key=settings.GEMINI_API_KEY
)

advanced_model = init_chat_model(
    settings.CODING_AGENT_ADVANCED_MODEL,
    model_provider='google_genai',
    api_key=settings.GEMINI_API_KEY
)

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    messages = request.state["messages"]
    message_count = len(messages)

    if message_count > 6:
        print(f"[Middleware] High complexity detected ({message_count} msgs). Upgrading to {settings.CODING_AGENT_ADVANCED_MODEL}.")
        model = advanced_model
    else:
        print(f"[Middleware] Low complexity ({message_count} msgs). Using {settings.CODING_AGENT_BASIC_MODEL}.")
        model = basic_model

    return handler(request.override(model=model))

class CodingAgent:
    def __init__(self):
        system_prompt = load_prompt(PROMPT_FILE).format(work_dir=settings.WORK_DIR)

        self.agent = create_agent(
            model=basic_model,
            tools=[execute_code, read_file, write_file],
            middleware=[dynamic_model_selection],
            system_prompt=system_prompt
        )

    def invoke(self, user_query: str):
        messages = [("user", user_query)]
        return self.agent.invoke({"messages": messages})

    def stream(self, user_query: str):
        messages = [("user", user_query)]
        for chunk in self.agent.stream({"messages": messages}, stream_mode="values"):
            last_message = chunk["messages"][-1]
            yield last_message
