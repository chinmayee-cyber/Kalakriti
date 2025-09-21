from google.adk import LlmAgent
from typing import Dict, Any, List
from agents.trend_agent import retrieve_insights_via_rag, get_comparables_from_local_index

def get_trends_for_artwork(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    return retrieve_insights_via_rag(metadata, k=3)

def get_comparables(embedding: List[float]) -> List[Dict[str, Any]]:
    return get_comparables_from_local_index(embedding, k=5)

price_prediction_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="price_prediction_agent",
    description="Predicts the estimated price of an artwork and explains reasoning, using RAG insights and comparables.",
    instruction="""
You are an art valuation assistant. 
Your task is to predict the price of a new artwork based only on:
- insights retrieved from the RAG corpus (medium trends, artist trends, size bucket trends)
- comparable artworks retrieved from the local embedding index

Steps you MUST follow:
1. Look at the trend insights provided (median prices, multipliers, sample sizes).
2. Look at the comparable artworks (their sale prices and metadata).
3. Combine these signals logically to produce a single estimated price range for the input artwork.
4. Explain your reasoning clearly. Reference both the trends and the comparables in plain English.
5. If confidence is low due to lack of data, explicitly state that.

You must return a JSON object with two keys:
- "predicted_price": the estimated price as a number or range
- "reasoning": a clear explanation of how you arrived at that prediction
    """,
    tools=[get_trends_for_artwork, get_comparables]
)