import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from functools import lru_cache
from config.settings import Config

class ImageProcessor:
    """Optimized image processing utilities"""
    
    # Precomputed CSS color mapping for speed
    CSS_COLORS = {
        (0, 0, 0): 'black', (255, 255, 255): 'white', (255, 0, 0): 'red',
        (0, 255, 0): 'green', (0, 0, 255): 'blue', (255, 255, 0): 'yellow',
        (255, 165, 0): 'orange', (128, 0, 128): 'purple', (165, 42, 42): 'brown',
        (128, 128, 128): 'gray', (255, 192, 203): 'pink', (0, 255, 255): 'cyan'
    }
    
    @staticmethod
    @lru_cache(maxsize=Config.IMAGE_CACHE_SIZE)
    def get_dominant_colors_fast(img_hash: int, img_array_bytes: bytes) -> tuple:
        """
        Fast dominant color extraction with caching
        
        Args:
            img_hash: Hash of the image for caching
            img_array_bytes: Image array as bytes
            
        Returns:
            Tuple of dominant color names
        """
        img_array = np.frombuffer(img_array_bytes, dtype=np.uint8).reshape(-1, 3)
        
        # Downsample for speed
        if len(img_array) > 10000:
            indices = np.random.choice(len(img_array), 10000, replace=False)
            img_array = img_array[indices]
        
        # Use fewer clusters for speed
        kmeans = KMeans(n_clusters=Config.N_COLORS, random_state=42, n_init=3, max_iter=100)
        kmeans.fit(img_array)
        
        colors = kmeans.cluster_centers_.astype(int)
        color_names = []
        
        for color in colors:
            # Find closest predefined color for speed
            min_dist = float('inf')
            closest_color = 'gray'
            
            for css_rgb, name in ImageProcessor.CSS_COLORS.items():
                dist = sum((a - b) ** 2 for a, b in zip(color, css_rgb))
                if dist < min_dist:
                    min_dist = dist
                    closest_color = name
            
            color_names.append(closest_color)
        
        return tuple(set(color_names))
    
    @staticmethod
    def resize_image_for_clip(image: Image.Image, max_size: int = 224) -> Image.Image:
        """
        Resize image for faster CLIP processing
        
        Args:
            image: PIL Image to resize
            max_size: Maximum size for the longer dimension
            
        Returns:
            Resized PIL Image
        """
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        return image