from typing import Any
from langchain.agents import create_agent  # pyright: ignore[reportUnknownVariableType]
from langchain.agents.structured_output import ToolStrategy
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph.state import CompiledStateGraph   # pyright: ignore[reportMissingTypeStubs]
from advanced_rag_chatbot.agent.weather_advanced import CustomResponseFormat  # pyright: ignore[reportPrivateLocalImportUsage]
from advanced_rag_chatbot.models import claude
from advanced_rag_chatbot.responses import ResponseFormat
from advanced_rag_chatbot.tools import Context, get_user_location, get_user_role, get_weather_for_location
from advanced_rag_chatbot.middleware import dynamic_model_selection, debug, infinite_loop_detector, user_role_prompt  # pyright: ignore[reportUnknownVariableType, reportUnusedImport]

from langchain.agents.middleware.types import AgentState

import os
from dataclasses import asdict
from psycopg import Connection
from psycopg.rows import DictRow
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
import logging
log  = logging.getLogger(__name__)
PP = {"pretty_print": True}
DB_URI = "postgresql://ragbot@localhost:5432/raga"
pgurl = os.environ.get("RAGBOT_POSTGRES_CONNECTION", DB_URI)
pool: ConnectionPool[Connection[DictRow]] = ConnectionPool(
    conninfo=DB_URI, max_size=10, kwargs={"row_factory": dict_row}
)

SYSTEM_PROMPT = """Your are an expert weather forecaster, who speaks in riddles.

You have access to these tools:
- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location
- get_user_role: use this to get the user's role for determining response complexity.


If a user asks you for the weather, make sure you know the location. If you can't tell from the questions where they at, then use get_user_location to find their location."""

class WeatherAgent:

    def __init__(self):
        self.checkpointer: PostgresSaver = PostgresSaver(pool)
        self.checkpointer.setup()
        self.agent:  CompiledStateGraph[AgentState[ResponseFormat], Context, Any, Any[ResponseFormat]] = create_agent(
            model=claude,
            tools=[get_user_location, get_user_role, get_weather_for_location],
            system_prompt=SYSTEM_PROMPT,
            response_format=ToolStrategy(CustomResponseFormat),
            context_schema=Context,
            checkpointer=self.checkpointer,
            #middleware=[debug, user_role_prompt, dynamic_model_selection]
            middleware=[infinite_loop_detector, user_role_prompt, dynamic_model_selection]   # pyright: ignore[reportArgumentType]
        )

    def invoke(self, content: str):
        response = ''
        try:
            response = self.agent.invoke(  # pyright: ignore[reportUnknownMemberType]
                {"messages": [{"role": "user", "content": content}]},
                config={  # pyright: ignore[reportArgumentType]
                    "configurable": {"thread_id": "1"},
                    "max_iterations": 3,
                },
                context=Context(user_id="1")
            )

            log.debug("invoke agent response")
            log.debug(response, extra=PP)
            structed_response_dataclass = asdict(response['structured_response'])
            return structed_response_dataclass
        except Exception as e:
            print(e)
            raise(e)


