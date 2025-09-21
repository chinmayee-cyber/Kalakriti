"""
trend_analysis.py — Core trend analysis functionality for art valuation
"""

import numpy as np
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

def assign_size_buckets(df: pd.DataFrame, buckets: int = 3) -> pd.DataFrame:
    """Create simple quantile-based size buckets on 'area'"""
    df = df.copy()
    # handle missing area by setting to 0 (they'll be in smallest bucket); alternatively filter them out
    df["area_fill"] = df["area"].fillna(0.0)
    try:
        df["size_bucket"] = pd.qcut(df["area_fill"], q=buckets, labels=[f"size_{i+1}" for i in range(buckets)])
    except Exception:
        # fallback if qcut cannot split (e.g., too many identical areas) — simple cut by percentiles
        q = np.percentile(df["area_fill"], [33, 66])
        df["size_bucket"] = pd.cut(df["area_fill"], bins=[-1e9, q[0], q[1], 1e18], labels=[f"size_{i+1}" for i in range(buckets)])
    df.drop(columns=["area_fill"], inplace=True)
    return df


def compute_basic_trends(df: pd.DataFrame, top_artists_n: int = 50) -> List[Dict[str, Any]]:
    """
    Compute the minimal trends described in the PoC:
      - per medium: median price, N, median price_per_area, multiplier vs global median
      - per artist: top N artists only (others ignored)
      - per size_bucket: median price and N
    Returns a list of insight card dicts.
    """
    cards = []
    df_valid = df[df["value"].notna()].copy()
    global_median = float(df_valid["value"].median()) if not df_valid.empty else 0.0

    # Add price_per_area (avoid division by zero)
    df_valid["price_per_area"] = df_valid.apply(lambda r: (r["value"] / r["area"]) if pd.notna(r["area"]) and r["area"] > 0 else np.nan, axis=1)

    # 1) Medium-level trends
    med_groups = df_valid.groupby("medium")
    for medium, g in med_groups:
        if medium is None or g.empty:
            continue
        n = int(g.shape[0])
        median_price = float(g["value"].median())
        median_ppa = float(g["price_per_area"].median()) if g["price_per_area"].notna().any() else None
        multiplier = (median_price / global_median) if global_median > 0 else None
        confidence = "low" if n < 30 else "high"
        text = f"{medium} — median price ${median_price:,.0f} (N={n})."
        if median_ppa is not None and not np.isnan(median_ppa):
            text += f" Median price/area = ${median_ppa:,.2f}."
        if multiplier is not None:
            text += f" Multiplier vs global median = {multiplier:.2f}."
        text += f" Confidence: {confidence}."
        card = {
            "type": "aggregate",
            "scope": {"medium": medium},
            "metric": "median_price",
            "value": median_price,
            "sample_size": n,
            "confidence": confidence,
            "text": text,
            "provenance": {"created_at": datetime.utcnow().isoformat()}
        }
        cards.append(card)

    # 2) Artist-level trends (top N artists)
    artist_counts = df_valid["artist"].value_counts().nlargest(top_artists_n)
    top_artists = list(artist_counts.index)
    for artist in top_artists:
        g = df_valid[df_valid["artist"] == artist]
        if g.empty:
            continue
        n = int(g.shape[0])
        median_price = float(g["value"].median())
        median_ppa = float(g["price_per_area"].median()) if g["price_per_area"].notna().any() else None
        confidence = "low" if n < 30 else "high"
        text = f"Artist: {artist} — median price ${median_price:,.0f} (N={n})."
        if median_ppa is not None and not np.isnan(median_ppa):
            text += f" Median price/area = ${median_ppa:,.2f}."
        text += f" Confidence: {confidence}."
        card = {
            "type": "aggregate",
            "scope": {"artist": artist},
            "metric": "median_price",
            "value": median_price,
            "sample_size": n,
            "confidence": confidence,
            "text": text,
            "provenance": {"created_at": datetime.utcnow().isoformat()}
        }
        cards.append(card)

    # 3) Size-bucket trends
    size_groups = df_valid.groupby("size_bucket")
    for size_bkt, g in size_groups:
        if pd.isna(size_bkt) or g.empty:
            continue
        n = int(g.shape[0])
        median_price = float(g["value"].median())
        median_ppa = float(g["price_per_area"].median()) if g["price_per_area"].notna().any() else None
        confidence = "low" if n < 30 else "high"
        text = f"{size_bkt} artworks — median price ${median_price:,.0f} (N={n})."
        if median_ppa is not None and not np.isnan(median_ppa):
            text += f" Median price/area = ${median_ppa:,.2f}."
        text += f" Confidence: {confidence}."
        card = {
            "type": "aggregate",
            "scope": {"size_bucket": str(size_bkt)},
            "metric": "median_price",
            "value": median_price,
            "sample_size": n,
            "confidence": confidence,
            "text": text,
            "provenance": {"created_at": datetime.utcnow().isoformat()}
        }
        cards.append(card)

    return cards