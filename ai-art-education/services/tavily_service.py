import aiohttp
import asyncio
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging
from datetime import datetime, timedelta

from config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    title: str
    url: str
    content: str
    snippet: str
    source: str
    images: List[str]
    published_date: Optional[str] = None
    relevance_score: float = 0.0
    query_match: bool = False

class TavilyService:
    """Service for handling Tavily search API interactions with art-specific optimizations"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com"
        self.session = None
        self.cache = {}  # Simple in-memory cache
        self.cache_expiry = timedelta(minutes=30)  # Cache results for 30 minutes
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
            
    async def initialize(self):
        """Initialize the session if not using context manager"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None
            
    def _get_cache_key(self, query: str, **kwargs) -> str:
        """Generate a cache key from query and parameters"""
        params = sorted([f"{k}:{v}" for k, v in kwargs.items()])
        return f"{query}:{':'.join(params)}"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache entry is still valid"""
        if cache_key not in self.cache:
            return False
            
        cached_time, _ = self.cache[cache_key]
        return datetime.now() - cached_time < self.cache_expiry
    
    async def search_art_style(
        self,
        query: str,
        max_results: int = 6,
        include_images: bool = True,
        use_cache: bool = True,
        domains: Optional[List[str]] = None,
        time_range: str = "365d"
    ) -> List[SearchResult]:
        """
        Perform a specialized search for art styles with art-specific optimizations
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            include_images: Whether to include images in results
            use_cache: Whether to use cached results if available
            domains: Specific domains to search
            time_range: Time range for results (e.g., "365d", "30d", "7d")
            
        Returns:
            List of SearchResult objects
        """
        # Check cache first
        cache_key = self._get_cache_key(
            query, 
            max_results=max_results, 
            include_images=include_images,
            domains=domains,
            time_range=time_range
        )
        
        if use_cache and self._is_cache_valid(cache_key):
            _, results = self.cache[cache_key]
            logger.info(f"Using cached results for query: {query}")
            return results
            
        # Build the search query with art-specific enhancements
        enhanced_query = self._enhance_art_query(query)
        
        # Prepare request payload
        payload = {
            "q": enhanced_query,
            "limit": max_results,
            "include_images": include_images,
            "time_range": time_range,
            "topic": "arts"  # Focus on arts topics
        }
        
        if domains:
            payload["domains"] = domains
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Make the API request
            async with self.session.post(
                f"{self.base_url}/v1/search",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Tavily API error: {response.status} - {error_text}")
                    raise Exception(f"Tavily API error: {response.status}")
                
                data = await response.json()
                
                # Process and enrich the results
                results = self._process_art_results(data, query)
                
                # Cache the results
                self.cache[cache_key] = (datetime.now(), results)
                
                return results
                
        except asyncio.TimeoutError:
            logger.error("Tavily search request timed out")
            raise Exception("Search request timed out")
        except aiohttp.ClientError as e:
            logger.error(f"HTTP error during Tavily search: {e}")
            raise Exception(f"HTTP error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during Tavily search: {e}")
            raise
    
    def _enhance_art_query(self, query: str) -> str:
        """
        Enhance the query with art-specific terms to improve relevance
        
        Args:
            query: Original query
            
        Returns:
            Enhanced query string
        """
        # Common art-related terms to boost relevance
        art_terms = [
            "art style", "techniques", "tutorial", "guide", "history",
            "characteristics", "materials", "painting", "drawing",
            "traditional", "modern", "contemporary", "folk art"
        ]
        
        # Remove any existing art terms to avoid duplication
        base_query = query.lower()
        for term in art_terms:
            base_query = base_query.replace(term, "")
            
        # Add the most relevant art terms
        enhanced_query = f"{base_query} art style techniques history"
        
        return enhanced_query.strip()
    
    def _process_art_results(self, data: Dict, original_query: str) -> List[SearchResult]:
        """
        Process and enrich Tavily API results for art-related content
        
        Args:
            data: Raw API response data
            original_query: The original search query
            
        Returns:
            List of processed SearchResult objects
        """
        results = []
        
        for item in data.get("results", [])[:10]:  # Limit to top 10 results
            # Extract basic information
            title = item.get("title", "No title")
            url = item.get("url", "")
            content = item.get("content", "")
            snippet = item.get("snippet", content[:200] if content else "")
            source = item.get("source", "")
            images = item.get("images", [])
            
            # Calculate relevance score for art content
            relevance_score = self._calculate_art_relevance(
                title, content, original_query
            )
            
            # Check if the result directly matches the query
            query_match = self._check_query_match(title, content, original_query)
            
            # Create SearchResult object
            result = SearchResult(
                title=title,
                url=url,
                content=content,
                snippet=snippet,
                source=source,
                images=images,
                relevance_score=relevance_score,
                query_match=query_match
            )
            
            results.append(result)
        
        # Sort by relevance score (highest first)
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return results
    
    def _calculate_art_relevance(self, title: str, content: str, query: str) -> float:
        """
        Calculate a relevance score for art-related content
        
        Args:
            title: Result title
            content: Result content
            query: Original search query
            
        Returns:
            Relevance score between 0.0 and 1.0
        """
        score = 0.0
        text = f"{title} {content}".lower()
        query_terms = query.lower().split()
        
        # Art-specific relevance factors
        art_keywords = [
            "art style", "technique", "painting", "drawing", "tutorial",
            "guide", "history", "characteristics", "materials", "step by step",
            "how to", "traditional", "modern", "contemporary", "folk art"
        ]
        
        # Score based on query term matches
        for term in query_terms:
            if term in text:
                score += 0.1
                
        # Score based on art-specific keywords
        for keyword in art_keywords:
            if keyword in text:
                score += 0.05
                
        # Bonus for tutorial/guide content
        if any(x in text for x in ["tutorial", "guide", "how to"]):
            score += 0.1
            
        # Bonus for historical/cultural context
        if any(x in text for x in ["history", "origin", "cultural", "traditional"]):
            score += 0.05
            
        # Cap the score at 1.0
        return min(score, 1.0)
    
    def _check_query_match(self, title: str, content: str, query: str) -> bool:
        """
        Check if the result directly matches the query
        
        Args:
            title: Result title
            content: Result content
            query: Original search query
            
        Returns:
            Boolean indicating direct match
        """
        query_terms = query.lower().split()
        text = f"{title} {content}".lower()
        
        # Check if all query terms appear in the text
        return all(term in text for term in query_terms)
    
    async def search_multiple_art_styles(
        self,
        queries: List[str],
        max_results_per_query: int = 3,
        include_images: bool = True
    ) -> Dict[str, List[SearchResult]]:
        """
        Search for multiple art styles concurrently
        
        Args:
            queries: List of search queries
            max_results_per_query: Maximum results per query
            include_images: Whether to include images
            
        Returns:
            Dictionary mapping queries to search results
        """
        tasks = []
        
        for query in queries:
            task = self.search_art_style(
                query, 
                max_results=max_results_per_query,
                include_images=include_images
            )
            tasks.append(task)
            
        # Execute all searches concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        processed_results = {}
        for query, result in zip(queries, results):
            if isinstance(result, Exception):
                logger.error(f"Error searching for '{query}': {result}")
                processed_results[query] = []
            else:
                processed_results[query] = result
                
        return processed_results
    
    async def get_art_style_overview(
        self,
        style_name: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Get a comprehensive overview of an art style by combining multiple search results
        
        Args:
            style_name: Name of the art style
            max_results: Number of results to include
            
        Returns:
            Structured overview of the art style
        """
        # Search for different aspects of the art style
        aspects = [
            f"{style_name} art style history",
            f"{style_name} art techniques",
            f"{style_name} art materials",
            f"{style_name} art characteristics",
            f"{style_name} art tutorial"
        ]
        
        # Search for all aspects
        all_results = []
        for aspect in aspects:
            try:
                results = await self.search_art_style(
                    aspect, 
                    max_results=2,  # Fewer results per aspect
                    include_images=False
                )
                all_results.extend(results)
            except Exception as e:
                logger.warning(f"Failed to search aspect '{aspect}': {e}")
                
        # Remove duplicates by URL
        unique_results = {}
        for result in all_results:
            if result.url not in unique_results:
                unique_results[result.url] = result
                
        # Get top results by relevance
        sorted_results = sorted(
            unique_results.values(), 
            key=lambda x: x.relevance_score, 
            reverse=True
        )[:max_results]
        
        # Extract key information
        overview = {
            "style_name": style_name,
            "sources": [{"title": r.title, "url": r.url} for r in sorted_results],
            "key_characteristics": self._extract_key_characteristics(sorted_results),
            "common_techniques": self._extract_techniques(sorted_results),
            "typical_materials": self._extract_materials(sorted_results),
            "historical_context": self._extract_history(sorted_results),
            "learning_resources": self._extract_tutorials(sorted_results)
        }
        
        return overview
    
    def _extract_key_characteristics(self, results: List[SearchResult]) -> List[str]:
        """Extract key characteristics from search results"""
        characteristics = set()
        characteristic_keywords = ["characterized by", "features", "known for", "distinctive"]
        
        for result in results:
            content = f"{result.title} {result.content}".lower()
            
            # Simple pattern matching for characteristics
            if "geometric" in content:
                characteristics.add("Geometric patterns")
            if "bold lines" in content or "line work" in content:
                characteristics.add("Bold lines")
            if "vibrant colors" in content or "bright colors" in content:
                characteristics.add("Vibrant colors")
            if "natural motifs" in content or "nature themes" in content:
                characteristics.add("Nature themes")
            if "symbolic" in content or "symbolism" in content:
                characteristics.add("Symbolic elements")
                
        return list(characteristics)
    
    def _extract_techniques(self, results: List[SearchResult]) -> List[str]:
        """Extract techniques from search results"""
        techniques = set()
        technique_keywords = ["technique", "method", "approach", "process"]
        
        for result in results:
            content = f"{result.title} {result.content}".lower()
            
            # Simple pattern matching for techniques
            if "brushwork" in content or "brush work" in content:
                techniques.add("Brushwork")
            if "line drawing" in content:
                techniques.add("Line drawing")
            if "stippling" in content:
                techniques.add("Stippling")
            if "cross-hatching" in content or "hatching" in content:
                techniques.add("Hatching")
            if "wash" in content and "ink" in content:
                techniques.add("Ink wash")
                
        return list(techniques)
    
    def _extract_materials(self, results: List[SearchResult]) -> List[str]:
        """Extract materials from search results"""
        materials = set()
        material_keywords = ["material", "paint", "ink", "paper", "canvas", "pigment"]
        
        for result in results:
            content = f"{result.title} {result.content}".lower()
            
            # Simple pattern matching for materials
            if "natural pigments" in content:
                materials.add("Natural pigments")
            if "rice paper" in content:
                materials.add("Rice paper")
            if "bamboo brush" in content or "bamboo pen" in content:
                materials.add("Bamboo tools")
            if "handmade paper" in content:
                materials.add("Handmade paper")
            if "acrylic" in content:
                materials.add("Acrylic paint")
            if "watercolor" in content:
                materials.add("Watercolor")
                
        return list(materials)
    
    def _extract_history(self, results: List[SearchResult]) -> str:
        """Extract historical context from search results"""
        history_snippets = []
        
        for result in results:
            content = f"{result.title} {result.content}"
            
            # Look for historical context
            history_indicators = ["origin", "originated", "history", "historical", "traditional", "ancient"]
            
            if any(indicator in content.lower() for indicator in history_indicators):
                # Take the first 200 characters around the first history indicator
                for indicator in history_indicators:
                    if indicator in content.lower():
                        start = max(0, content.lower().find(indicator) - 100)
                        end = min(len(content), start + 300)
                        snippet = content[start:end].strip()
                        history_snippets.append(snippet)
                        break
        
        # Combine snippets
        if history_snippets:
            return " ".join(history_snippets)[:500] + "..."
        else:
            return "Historical context not found in search results."
    
    def _extract_tutorials(self, results: List[SearchResult]) -> List[Dict[str, str]]:
        """Extract tutorial resources from search results"""
        tutorials = []
        tutorial_keywords = ["tutorial", "guide", "how to", "step by step", "learn"]
        
        for result in results:
            content = f"{result.title} {result.content}".lower()
            
            if any(keyword in content for keyword in tutorial_keywords):
                tutorials.append({
                    "title": result.title,
                    "url": result.url,
                    "snippet": result.snippet[:150] + "..." if len(result.snippet) > 150 else result.snippet
                })
                
        return tutorials
    
    def clear_cache(self):
        """Clear the search cache"""
        self.cache = {}


# Singleton instance for easy access
tavily_service = TavilyService()