import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class Config:
    """Configuration class with environment variables"""
    MONGO_URI: str = os.getenv('MONGO_URI')
    DB_NAME: str = os.getenv('DB_NAME', 'art_database')
    COLLECTION_NAME: str = os.getenv('COLLECTION_NAME', 'artworks')
    BATCH_SIZE: int = int(os.getenv('BATCH_SIZE', '20'))
    MAX_WORKERS: int = int(os.getenv('MAX_WORKERS', str(os.cpu_count())))
    CONFIDENCE_THRESHOLD: float = float(os.getenv('CONFIDENCE_THRESHOLD', '0.1'))
    N_COLORS: int = int(os.getenv('N_COLORS', '4'))
    CLIP_MODEL: str = os.getenv('CLIP_MODEL', 'ViT-B/32')
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '10'))
    IMAGE_CACHE_SIZE: int = int(os.getenv('IMAGE_CACHE_SIZE', '100'))
    
    # Label configurations
    STYLE_LABELS: str = os.getenv('STYLE_LABELS', 'Impressionism,Realism,Abstract,Expressionism,Surrealism,Cubism,Pop Art,Minimalism,Contemporary,Traditional')
    SUBJECT_LABELS: str = os.getenv('SUBJECT_LABELS', 'Landscape painting,Portrait,Still life,Abstract art,Seascape,Cityscape,Nature scene,Animal painting')
    COMPOSITION_OBJECTS: str = os.getenv('COMPOSITION_OBJECTS', 'tree,mountain,building,person,animal,flower,boat,bridge,house,rock,cloud,river,ocean,beach,forest,sky')
    LIGHTING_CONDITIONS: str = os.getenv('LIGHTING_CONDITIONS', 'bright sunlight,soft diffuse light,dramatic lighting,golden hour,sunset lighting,morning light,overcast')
    TEXTURE_DESCRIPTIONS: str = os.getenv('TEXTURE_DESCRIPTIONS', 'smooth brush strokes,rough brush strokes,thick impasto,fine detailed brushwork,loose brushwork,visible brush marks')
    BACKGROUND_LABELS: str = os.getenv('BACKGROUND_LABELS', 'mountains,sky,forest,ocean,city,abstract background')