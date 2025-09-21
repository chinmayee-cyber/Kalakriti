import numpy as np
import joblib
from typing import List, Dict, Any, Optional
from sklearn.neighbors import NearestNeighbors

class ImageEmbeddingIndex:
    def __init__(self, n_neighbors=5, metric="cosine"):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.model: Optional[NearestNeighbors] = None
        self.ids: List[str] = []
        self.embeddings: Optional[np.ndarray] = None
        self.meta: Dict[str, Dict[str, Any]] = {}

    def build(self, id_list: List[str], embedding_list: List[List[float]], meta_list: List[Dict[str, Any]]):
        if not id_list:
            raise RuntimeError("No embeddings provided to build index.")
        self.ids = id_list
        self.embeddings = np.array(embedding_list).astype(float)
        self.model = NearestNeighbors(n_neighbors=self.n_neighbors, metric=self.metric)
        self.model.fit(self.embeddings)
        for _id, m in zip(id_list, meta_list):
            self.meta[_id] = m

    def save(self, path: str):
        joblib.dump({
            "ids": self.ids,
            "embeddings": self.embeddings,
            "meta": self.meta,
            "model": self.model
        }, path)

    def load(self, path: str):
        data = joblib.load(path)
        self.ids = data["ids"]
        self.embeddings = data["embeddings"]
        self.meta = data["meta"]
        self.model = data["model"]

    def query(self, q_embedding: List[float], k: int = 5) -> List[Dict[str, Any]]:
        if self.model is None:
            raise RuntimeError("Index not built/loaded.")
        q = np.array(q_embedding).reshape(1, -1).astype(float)
        dists, idxs = self.model.kneighbors(q, n_neighbors=min(k, len(self.ids)))
        results = []
        for dist, idx in zip(dists[0], idxs[0]):
            _id = self.ids[int(idx)]
            results.append({
                "artwork_id": _id,
                "distance": float(dist),
                "meta": self.meta.get(_id, {})
            })
        return results