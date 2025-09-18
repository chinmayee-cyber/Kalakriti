"""
Valuation Agent
- Takes an artwork_id, ensures metadata is present (calls MetadataAgent if needed),
  fetches feature data (artist aggregate or whatever exists), and returns a predicted value
  plus interval and explanation.
"""

from google.adk.agents import Agent, Tool
from art_meta.config import Config
from pymongo import MongoClient
import logging
import math

logger = logging.getLogger(__name__)

class ValuationAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        self.art_col = self.db[Config.COLLECTION_NAME]
        self.features_col = self.db.get_collection("features")
        self.valuations_col = self.db.get_collection("valuations")

    @Tool(name="valuate", description="Return estimation for artwork given artwork_id")
    def valuate(self, artwork_id: str) -> dict:
        """
        For given artwork_id:
         - If metadata missing, return error or instruct to generate it.
         - If model prediction present in valuations collection, return that.
         - Otherwise fallback: use artist average price if available, or existing fields.
         - Return predicted_price, lower and upper intervals, explanation.
        """
        art = self.art_col.find_one({"_id": artwork_id})
        if not art:
            return {"ok": False, "error": "artwork not found"}

        # ensure metadata exists
        if "metadata" not in art:
            return {"ok": False, "error": "metadata missing; run MetadataAgent first"}

        # check for existing valuation
        existing = self.valuations_col.find_one({"artwork_id": artwork_id})
        if existing:
            return {
                "ok": True,
                "predicted_price": existing.get("predicted_price"),
                "lower_q": existing.get("lower_q"),
                "upper_q": existing.get("upper_q"),
                "explainability": existing.get("explainability", {})
            }

        # fallback heuristic
        # attempt to fetch artist aggregates
        feat = self.features_col.find_one({"artwork_id": artwork_id})
        if feat and feat.get("artist_avg_price"):
            base_price = feat["artist_avg_price"]
            method = "artist_avg"
        else:
            base_price = art.get("winning_bid") or art.get("value") or 0
            method = "historical_bid_or_value"

        # interval ±30%
        lower = math.floor(base_price * 0.7)
        upper = math.ceil(base_price * 1.3)

        explanation = {
            "method": method,
            "basis_value": base_price
        }

        return {
            "ok": True,
            "predicted_price": base_price,
            "lower_q": lower,
            "upper_q": upper,
            "explainability": explanation
        }
