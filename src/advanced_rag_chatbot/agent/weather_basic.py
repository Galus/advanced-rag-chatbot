from langchain.agents import create_agent
from langchain_core.messages import AIMessage

class WeatherBasicAgent:
    def __init__(self):
        tools = [self.get_weather]
        self.agent = create_agent(
            model="claude-sonnet-4-5-20250929",
            tools=tools,
            system_prompt="You are a helpful assistant"
        )

    def get_weather(self, city: str) -> str:
        """Get weather for a given city."""
        return f"It's always sunny in {city}!"

    def invoke(self, content: str):
        resp = ''
        try:
            resp = self.agent.invoke(
                    {"messages": [{"role": "user", "content": content}]}
            )
            messages = resp['messages']
            msgs = []
            for msg in messages:
                if msg['AIMessage']:
                    msgs.append(msg['content'])

            return resp
        except Exception as e:
            print(e)
            print(resp)
            raise(e)



