import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "art_db")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "artworks")
CORPUS_DISPLAY_NAME = os.getenv("RAG_CORPUS", "ArtValuation_PoC_Corpus")