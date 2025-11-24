from langchain.chat_models import init_chat_model
import os

if "MODEL_TEMP" not in os.environ:
    os.environ["MODEL_TEMP"] = "0.5"

claude = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature=float(os.environ["MODEL_TEMP"]),
    timeout=10,
    max_tokens=1000
)

gemini = init_chat_model(
    "gemini-2.5-flash",
    temperature=float(os.environ["MODEL_TEMP"]),
    max_tokens=1000,
    max_retries=2
)
