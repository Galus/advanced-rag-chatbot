from dataclasses import dataclass

@dataclass
class ResponseFormat:
    riddle_response: str
    weather_conditions: str | None = None
