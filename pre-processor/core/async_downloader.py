import aiohttp
from PIL import Image
from io import BytesIO
from typing import Optional
import asyncio
from config.settings import Config

class AsyncImageDownloader:
    """Async image downloader for better performance"""
    
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=20)
        timeout = aiohttp.ClientTimeout(total=Config.REQUEST_TIMEOUT)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def download_image(self, url: str) -> Optional[Image.Image]:
        """
        Download image asynchronously
        
        Args:
            url: Image URL to download
            
        Returns:
            PIL Image or None if download fails
        """
        async with self.semaphore:
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        return Image.open(BytesIO(content)).convert('RGB')
            except Exception as e:
                print(f"Error downloading {url}: {e}")
                return None