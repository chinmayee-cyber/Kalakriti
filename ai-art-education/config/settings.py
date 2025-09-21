import os
from dataclasses import dataclass

@dataclass
class Settings:
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    GCP_PROJECT: str = os.getenv("GCP_PROJECT", "")
    LLM_MODEL: str = "gemini-2.0-flash-thinking-exp"
    LLM_TEMPERATURE: float = 0.2
    
settings = Settings()