from langchain.agents import create_agent
from langchain.agents.middleware.types import ModelRequest, ModelResponse, wrap_model_call
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import InMemorySaver
from advanced_rag_chatbot.agent.weather_advanced import CustomResponseFormat
from advanced_rag_chatbot.models import claude, gemini
from advanced_rag_chatbot.tools import Context, get_user_location, get_weather_for_location
from dataclasses import asdict
import logging
log = logging.getLogger(__name__)
PP = {"pretty_print": True}

basic_model = claude
advanced_model = gemini
SYSTEM_PROMPT = """Your are an expert weather forecaster, who speaks in riddles.

You have access to two tools:
- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can't tell from the questions where they at, then use get_user_location to find their location."""

@wrap_model_call
def dynamic_model_selection(req: ModelRequest, handler) -> ModelResponse:
    message_count = len(req.state["messages"])
    log.debug(f"message_count: {message_count}")
    if message_count > 1:
        model = advanced_model
    else:
        model = basic_model

    return handler(req.override(model=model))

class WeatherAgent:
    def __init__(self):
        self.agent = create_agent(
            model=basic_model,
            tools=[get_user_location, get_weather_for_location],
            system_prompt=SYSTEM_PROMPT,
            response_format=ToolStrategy(CustomResponseFormat),
            context_schema=Context, # pyright: ignore
            checkpointer=InMemorySaver(),
            middleware=[dynamic_model_selection] # pyright: ignore
        )

    def invoke(self, content: str):
        response = ''
        try:
            response = self.agent.invoke(
                    {"messages": [{"role": "user", "content": content}]},
                config={"configurable": {"thread_id": "1"}},
                context=Context(user_id="1")
            )

            log.debug("invoke agent response")
            log.debug(response, extra=PP)
            structed_response_dataclass = asdict(response['structured_response'])
            return structed_response_dataclass
        except Exception as e:
            print(e)
            raise(e)


