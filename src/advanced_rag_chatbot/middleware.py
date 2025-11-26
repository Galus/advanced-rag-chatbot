from dataclasses import asdict
from typing import Callable, Any, cast
from langchain.agents.middleware.types import ModelRequest, ModelResponse, dynamic_prompt, wrap_model_call
from langchain_core.messages import AIMessage
from advanced_rag_chatbot.models import claude, gemini
from advanced_rag_chatbot.responses import ResponseFormat as CustomResponseFormat
import logging
from advanced_rag_chatbot.tools import Context as MyContext
log = logging.getLogger(__name__)

# Raw 
@wrap_model_call
def debug(request: ModelRequest, handler) -> ModelResponse:
    log.debug(f"req: {request}")
    return handler(request)

@wrap_model_call
def infinite_loop_detector(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
        threshold: int = 5
) -> ModelResponse:
    history = []
    for message in reversed(request.messages):
        if isinstance(message, AIMessage) and message.tool_calls:
            tool_call = message.tool_calls[0]
            history.append((tool_call['name'], tuple(tool_call['args'].items())))
            if len(history) >= threshold:
                break

    is_looping = len(history) >= (threshold-1) and all(action == history[0] for action in history)
    if is_looping:
        tool_name = history[0][0]
        final_answer = (
            f"I appear to be going in circles trying to use '{tool_name}' tool."
            " Please ask me a different question."
        )

        loopy_structured_response = CustomResponseFormat(
            riddle_response=final_answer,
            weather_conditions=None
        )

        return ModelResponse(
            result=[AIMessage(content=final_answer)],
            structured_response=loopy_structured_response,
        )

    return handler(request)

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    message_count = len(request.state["messages"])
    log.debug(f"message_count: {message_count}")
    if message_count > 1:
        model = gemini
    else:
        model = claude

    return handler(request.override(model=model))

# Prompts
@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    ctx: MyContext = cast(MyContext, request.runtime.context)
    user_role = ctx.user_role
    log.debug(f"user_role: {user_role}")
    base_prompt = "You are a helpful assistant."

    if user_role == "expert":
        return f"{base_prompt} Provide detailed technical responses."
    elif user_role == "beginner":
        return f"{base_prompt} Explain concepts simply and avoid technical jargon."
    
    return base_prompt
