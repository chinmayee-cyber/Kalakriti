import os
from dataclasses import dataclass

@dataclass
class Settings:
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")
    
settings = Settings()