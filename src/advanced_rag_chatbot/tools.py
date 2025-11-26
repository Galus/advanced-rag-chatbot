from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

import logging
log = logging.getLogger(__name__)

@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str
    user_role: str = "beginner"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    log.debug(f"get_user_location called with {runtime}")
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

@tool
def get_user_role(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    log.debug(f"get_user_role called with {runtime}")
    user_role = runtime.context.user_role
    if user_role == "":
        return "beginner"
    else:
        return str(user_role)
