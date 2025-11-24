from advanced_rag_chatbot.agent.weather import WeatherAgent
from advanced_rag_chatbot.custom_logging import configure_root_pprint_logger
from advanced_rag_chatbot.agent.weather_advanced import WeatherAgentAdvanced
from advanced_rag_chatbot.agent.weather_basic import WeatherBasicAgent
import pprint

import logging
configure_root_pprint_logger()
log = logging.getLogger(__name__)


def main():
    print("Hello from advanced-rag-chatbot!")

    # log.info("Basic Weather Agent")
    # weather_agent = WeatherBasicAgent()
    # resp = weather_agent.invoke("What is the weather in Pidgeon Forge, TN?")
    # log.info(resp)

    # log.info("Advanced Weather Agent")
    # weather_agent_v2 = WeatherAgentAdvanced()
    # resp = weather_agent_v2.invoke("What is the weather in Apex, NC?")
    # log.info(resp)

    log.info("MultiModel Agent")
    weather_agent_v3 = WeatherAgent()
    log.info("Ask the agent about the weather in some area.")
    user_text = input()
    resp = weather_agent_v3.invoke(user_text)
    log.info(resp)

    print("Goodbye from advanced-rag-chatbot!")

if __name__ == "__main__":
    main()
