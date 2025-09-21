import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv() 

@dataclass
class Settings:
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY") 
    
settings = Settings()