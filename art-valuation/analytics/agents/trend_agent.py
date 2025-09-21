import os
import tempfile
import json
from typing import List, Dict, Any
from database.db_manager import load_artworks_from_mongo
from services.rag import initialize_vertex_ai, create_or_get_corpus, upload_text_file_to_corpus
from services.trend_analysis import assign_size_buckets, compute_basic_trends
from database.embeddings import ImageEmbeddingIndex
from config.settings import CORPUS_DISPLAY_NAME

import numpy as np
import pandas as pd

def write_insight_cards_to_tempfiles(cards: List[Dict[str, Any]], temp_dir: str) -> List[str]:
    file_paths = []
    for i, card in enumerate(cards):
        fname = f"insight_card_{i+1}.txt"
        path = os.path.join(temp_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(card["text"].strip() + "\n\n")
            f.write("---METADATA---\n")
            f.write(json.dumps(card["scope"]) + "\n")
            f.write(json.dumps({
                "metric": card.get("metric"),
                "value": card.get("value"),
                "sample_size": card.get("sample_size"),
                "confidence": card.get("confidence"),
                "provenance": card.get("provenance"),
            }) + "\n")
        file_paths.append(path)
    return file_paths

def run_trend_agent_one_shot():
    initialize_vertex_ai()
    corpus = create_or_get_corpus(CORPUS_DISPLAY_NAME)
    
    df = load_artworks_from_mongo()
    df = assign_size_buckets(df, buckets=3)
    cards = compute_basic_trends(df, top_artists_n=50)
    
    with tempfile.TemporaryDirectory() as td:
        file_paths = write_insight_cards_to_tempfiles(cards, td)
        for path in file_paths:
            display_name = os.path.basename(path)
            description = "PoC insight card"
            upload_text_file_to_corpus(corpus.name, path, display_name, description)
    
    # Build image embedding index
    df_emb = df[df["img_embedding"].notna() & df["_id"].notna()].copy()
    ids = df_emb["_id"].astype(str).tolist()
    embeddings = [np.array(e).astype(float).tolist() for e in df_emb["img_embedding"].tolist()]
    meta_list = []
    for _, row in df_emb.iterrows():
        meta_list.append({
            "sale_price": float(row["value"]) if pd.notna(row["value"]) else None,
            "artist": row.get("artist"),
            "medium": row.get("medium"),
            "size_bucket": str(row.get("size_bucket")),
            "mongo_id": str(row["_id"])
        })

    img_index = ImageEmbeddingIndex(n_neighbors=5, metric="cosine")
    if ids:
        img_index.build(ids, embeddings, meta_list)
        index_path = os.path.join(os.getcwd(), "image_embedding_index.joblib")
        img_index.save(index_path)
    
    return {"status": "success", "cards_uploaded": len(cards)}

def retrieve_insights_via_rag(query_filters: Dict[str, str], k: int = 3) -> List[Dict[str, Any]]:
    qtext = " ".join([f"{k}:{v}" for k, v in query_filters.items()])
    return [{"text": f"Retrieved insight for {qtext} (PoC placeholder)", "meta": query_filters}]

def get_comparables_from_local_index(query_embedding: List[float], k: int = 5, 
                                    index_path: str = "image_embedding_index.joblib") -> List[Dict[str, Any]]:
    idx = ImageEmbeddingIndex()
    idx.load(index_path)
    return idx.query(query_embedding, k=k)