import logging
import time
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import requests
from io import BytesIO
from PIL import Image
import numpy as np
from config.settings import Config

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def download_image_sync(url: str) -> Optional[Image.Image]:
    """
    Synchronous image download
    
    Args:
        url: Image URL to download
        
    Returns:
        PIL Image or None if download fails
    """
    try:
        response = requests.get(url, timeout=Config.REQUEST_TIMEOUT)
        response.raise_for_status()
        return Image.open(BytesIO(response.content)).convert('RGB')
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def process_batch(batch: List[Dict], process_function, max_workers: int = None) -> List:
    """
    Process a batch of items using ThreadPoolExecutor
    
    Args:
        batch: List of items to process
        process_function: Function to process each item
        max_workers: Maximum number of worker threads
        
    Returns:
        List of processed results
    """
    if max_workers is None:
        max_workers = Config.MAX_WORKERS
        
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(process_function, batch))

def create_mongodb_indexes(collection):
    """
    Create MongoDB indexes for better query performance
    
    Args:
        collection: MongoDB collection object
    """
    indexes = [
        [("metadata.style_labels", 1)],
        [("metadata.dominant_colors", 1)],
        [("metadata.medium_labels", 1)],
        [("metadata.caption", "text")],
        [("metadata.composition.background", 1)],
        [("metadata.lighting", 1)],
        [("metadata.texture", 1)]
    ]
    
    for index in indexes:
        try:
            collection.create_index(index)
        except:
            pass  # Index might already exist
    
    print("MongoDB indexes created/verified")