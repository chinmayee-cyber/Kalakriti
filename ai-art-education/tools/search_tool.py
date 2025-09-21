import aiohttp
from typing import List, Dict, Any, Optional
from config import settings

class TavilySearchTool:
    """Enhanced Tavily search tool with async support"""
    
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com/v1/search"
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, *args):
        await self.session.close()
        
    async def search_art_style(
        self, 
        style_query: str,
        max_results: int = 5,
        include_images: bool = True
    ) -> List[Dict[str, Any]]:
        """Specialized search for art styles"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": f"{style_query} art style tutorial techniques history",
            "limit": max_results,
            "include_images": include_images,
            "time_range": "365d",
            "topic": "arts"
        }
        
        async with self.session.post(
            self.base_url, 
            headers=headers, 
            json=payload
        ) as response:
            if response.status != 200:
                raise RuntimeError(f"Tavily search failed: {await response.text()}")
                
            data = await response.json()
            return self._process_art_results(data)
    
    def _process_art_results(self, data: Dict) -> List[Dict[str, Any]]:
        """Process and enrich art-specific results"""
        processed_results = []
        
        for item in data.get("results", []):
            processed_results.append({
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "images": item.get("images", []),
                "source": item.get("source", ""),
                "relevance_score": self._calculate_art_relevance(item)
            })
            
        return sorted(processed_results, key=lambda x: x["relevance_score"], reverse=True)
    
    def _calculate_art_relevance(self, item: Dict) -> float:
        """Calculate relevance score for art content"""
        score = 0.0
        content = (item.get("title", "") + " " + item.get("snippet", "")).lower()
        
        art_keywords = ["art style", "technique", "painting", "drawing", 
                       "tutorial", "guide", "history", "characteristics"]
        
        for keyword in art_keywords:
            if keyword in content:
                score += 0.1
                
        return min(score, 1.0)