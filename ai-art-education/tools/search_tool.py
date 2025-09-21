# tools/search_tool.py
import asyncio
import functools
import logging
from typing import List, Dict, Any, Optional

from tavily import TavilyClient
from config import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TavilySearchTool:
    """
    Async wrapper around TavilyClient with:
      - concurrency control (semaphore)
      - simple in-memory TTL cache
      - normalized search result shape: {title, snippet, url, source, published_at}
      - helper to format top-k search results into a RAG-friendly string

    Usage:
        tool = TavilySearchTool()
        results = await tool.search("Warli motifs", max_results=6)
        rag_context = tool.format_for_rag(results)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        max_concurrency: int = 4,
        cache_ttl: int = 600,
    ):
        key = api_key or getattr(settings, "TAVILY_API_KEY", None)
        if not key:
            raise RuntimeError("TAVILY_API_KEY must be set in settings or passed to TavilySearchTool.")
        self.client = TavilyClient(api_key=key)
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._cache: Dict[str, Dict[str, Any]] = {}  # key -> {"expiry": float, "value": ...}
        self._cache_ttl = cache_ttl

    # --- internal helper: run sync client in threadpool ---
    async def _run_sync(self, fn, *args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, functools.partial(fn, *args, **kwargs))

    # --- public: general search ---
    async def search(
        self,
        query: str,
        max_results: int = 5,
        domains: Optional[List[str]] = None,
        time_range: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Run a Tavily search and return a list of normalized results.
        Normalized result keys: title, snippet, url, source, published_at
        """
        cache_key = f"tavily|{query}|{','.join(domains) if domains else ''}|{max_results}|{time_range}"
        now = asyncio.get_event_loop().time()
        cached = self._cache.get(cache_key)
        if cached and cached["expiry"] > now:
            return cached["value"]

        async with self._semaphore:
            try:
                # The TavilyClient sample in your snippet used a synchronous call:
                # tavily_client.search("Who is Leo Messi?")
                # so we call the synchronous method in an executor.
                # If your TavilyClient supports async, you can call it directly instead.
                raw = await self._run_sync(self.client.search, query)
            except Exception as exc:
                logger.exception("Tavily search failed for query=%s", query)
                raise

        # Normalize response shape. Tavily response shapes can vary by plan/version;
        # we attempt common keys and fall back gracefully.
        results: List[Dict[str, Any]] = []
        items = None
        # common response wrappers
        if isinstance(raw, dict):
            items = raw.get("results") or raw.get("items") or raw.get("hits") or raw.get("data")
        if items is None:
            # maybe raw itself is a list or dict with direct fields
            if isinstance(raw, list):
                items = raw
            else:
                items = [raw]

        for item in (items or [])[:max_results]:
            # multiple naming variants handled
            title = item.get("title") or item.get("headline") or item.get("name") or ""
            snippet = (
                item.get("snippet")
                or item.get("excerpt")
                or item.get("summary")
                or item.get("description")
                or ""
            )
            url = item.get("url") or item.get("link") or item.get("uri") or ""
            source = item.get("source") or item.get("domain") or item.get("host") or ""
            published_at = item.get("published_at") or item.get("date") or item.get("time") or None

            results.append(
                {
                    "title": title,
                    "snippet": snippet,
                    "url": url,
                    "source": source,
                    "published_at": published_at,
                    "raw": item,
                }
            )

        # cache and return
        self._cache[cache_key] = {"expiry": now + self._cache_ttl, "value": results}
        return results

    # --- convenience wrapper: search specifically for art style pages ---
    async def search_art_style(self, style_query: str, max_results: int = 6) -> List[Dict[str, Any]]:
        """
        Lightweight specialization for art-styles: search for tutorials, motifs, history, technique.
        Returns normalized results suitable for building a search_context.
        """
        q = f"{style_query} art techniques tutorial motifs history craft \"how to\""
        return await self.search(q, max_results=max_results)

    # --- helper: build RAG-friendly context string for LLM prompt ---
    def format_for_rag(self, results: List[Dict[str, Any]], max_chars: int = 2000) -> str:
        """
        Convert top results into a concatenated string useful for LLM grounding.
        Keeps items concise and respects max_chars.
        Example output chunk:
          Source 1: <title>
          Snippet: <snippet>
          URL: <url>
        """
        parts = []
        for i, r in enumerate(results[:10]):
            title = r.get("title") or "No title"
            snippet = (r.get("snippet") or "").strip().replace("\n", " ")
            url = r.get("url") or ""
            part = f"Source {i+1}: {title}\nContent: {snippet}\nURL: {url}\n"
            parts.append(part)
        joined = "\n".join(parts)
        if len(joined) > max_chars:
            return joined[: max_chars - 3] + "..."
        return joined

    # --- optional: clear cache (useful in tests/dev) ---
    def clear_cache(self):
        self._cache.clear()

    # --- ADK tool compatibility helper (optional) ---
    async def run(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Minimal tool-like interface returning a simple dict {ok: True/False, results: [...]}
        Useful if you want to register this object as an ADK tool or call generically.
        """
        try:
            results = await self.search(query, max_results=max_results)
            return {"ok": True, "results": results}
        except Exception as e:
            return {"ok": False, "error": str(e)}

