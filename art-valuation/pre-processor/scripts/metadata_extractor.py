#!/usr/bin/env python3

from typing import List, Dict
import os
import io
import requests
from PIL import Image
import numpy as np
import torch
import clip
from pymongo import MongoClient
from bson import ObjectId

# ========== Configuration (constants) ==========

class MongoConfig:
    URI = "mongodb+srv://shrijulv_db_user:databaseuser123@kalakriti.antxk6w.mongodb.net/"  # REPLACE
    DB_NAME = "datasets"                                         # REPLACE
    COLLECTION = "auction-sales"                              # REPLACE

# ========== CLIP embedding + zero-shot tags extractor ==========

def load_image(source: str, timeout: int = 10) -> Image.Image:
    """Load image from URL or local file path. Returns a PIL.Image in RGB."""
    if source.startswith("http://") or source.startswith("https://"):
        resp = requests.get(source, timeout=timeout)
        resp.raise_for_status()
        return Image.open(io.BytesIO(resp.content)).convert("RGB")
    else:
        if not os.path.exists(source):
            raise FileNotFoundError(f"File not found: {source}")
        return Image.open(source).convert("RGB")

class ClipWrapper:
    def __init__(self, model_name: str = "ViT-B/32", device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.preprocess = clip.load(model_name, device=self.device)
        self.model.eval()
        self.model_name = model_name

    @torch.no_grad()
    def get_image_embedding(self, pil_img: Image.Image) -> np.ndarray:
        """Return L2-normalized image embedding as a numpy array (dtype=float32)."""
        img_t = self.preprocess(pil_img).unsqueeze(0).to(self.device)  # 1 x C x H x W
        img_feat = self.model.encode_image(img_t)  # 1 x D (torch.Tensor)
        img_feat = img_feat.cpu().numpy().squeeze(0).astype(np.float32)
        norm = np.linalg.norm(img_feat) + 1e-12
        return img_feat / norm

    @torch.no_grad()
    def zero_shot_scores(self, pil_img: Image.Image, candidate_texts: List[str], top_k: int = 10
                        ) -> List[Dict[str, float]]:
        """
        Score candidate texts against the image using CLIP zero-shot approach.
        Returns list of top_k dicts: [{"label": str, "score": float}, ...]
        Scores are softmax probabilities (sum ~ 1 across candidates).
        """
        # encode image
        img_t = self.preprocess(pil_img).unsqueeze(0).to(self.device)
        img_feat = self.model.encode_image(img_t)  # 1 x D
        img_feat = img_feat / img_feat.norm(dim=-1, keepdim=True)

        # encode texts
        text_tokens = clip.tokenize(candidate_texts).to(self.device)  # N x token_len
        text_feat = self.model.encode_text(text_tokens)  # N x D
        text_feat = text_feat / text_feat.norm(dim=-1, keepdim=True)

        # similarity logits
        logits = (100.0 * img_feat @ text_feat.T).cpu().numpy().squeeze(0)  # shape: (N,)

        # convert to probabilities
        exps = np.exp(logits - np.max(logits))
        probs = exps / (np.sum(exps) + 1e-12)

        idxs = np.argsort(-probs)[: min(top_k, len(candidate_texts))]
        return [{"label": candidate_texts[i], "score": float(probs[i])} for i in idxs]

def extract_embedding_and_tags(image_source: str, candidate_texts: List[str], top_k: int = 6,
                               model_name: str = "ViT-B/32", device: str = None
                              ) -> Dict:
    """Returns embedding and zero_shot_tags for an image."""
    img = load_image(image_source)
    clip_w = ClipWrapper(model_name=model_name, device=device)
    embedding = clip_w.get_image_embedding(img)
    tags = clip_w.zero_shot_scores(img, candidate_texts, top_k=top_k)
    return {
        "image_embedding": embedding.tolist(),
        "embedding_dim": int(embedding.shape[0]),
        "embedding_model": clip_w.model_name,
        "zero_shot_tags": tags
    }

# ========== Candidate labels ==========

DEFAULT_CANDIDATES = [
    "landscape", "portrait", "seascape", "cityscape", "still life", "abstract",
    "figurative", "impressionist", "expressionist", "contemporary", "modern",
    "oil painting", "watercolor", "acrylic", "print", "photograph", "black and white",
    "colorful", "large", "small", "signed", "unsigned", "textured", "flat"
]

# ========== Main Mongo-update pipeline ==========

def process_document(doc: Dict, clip_wrapper: ClipWrapper, candidates: List[str]) -> Dict:
    """Given a Mongo document, produce the metadata to insert."""
    image_url = doc.get("img_url")
    if not image_url:
        raise ValueError(f"Document {doc.get('_id')} has no 'img_url' field.")
    metadata = extract_embedding_and_tags(image_url, candidate_texts=candidates, top_k=6,
                                          model_name=clip_wrapper.model_name, device=clip_wrapper.device)
    return metadata

def main():
    client = MongoClient(MongoConfig.URI)
    db = client[MongoConfig.DB_NAME]
    coll = db[MongoConfig.COLLECTION]

    clip_wrapper = ClipWrapper(model_name="ViT-B/32", device=None)

    cursor = coll.find({})  

    for doc in cursor:
        doc_id = doc.get("_id")
        if doc.get("metadata") and "image_embedding" in doc["metadata"] and "zero_shot_tags" in doc["metadata"]:
            print(f"Skipping document {doc_id} since metadata already present.")
            continue

        print(f"\nProcessing document _id: {doc_id}")
        try:
            metadata_to_add = process_document(doc, clip_wrapper, DEFAULT_CANDIDATES)
        except Exception as e:
            print(f"Error processing image for doc {doc_id}: {e}")
            continue

        print("Metadata to add:")
        print(metadata_to_add)

        user_input = input("Do you want to add this metadata to MongoDB? (y/n): ").strip().lower()
        if user_input == "y":
            result = coll.update_one(
                {"_id": doc_id},
                {"$set": {
                    "metadata.image_embedding": metadata_to_add["image_embedding"],
                    "metadata.embedding_dim": metadata_to_add.get("embedding_dim"),
                    "metadata.embedding_model": metadata_to_add.get("embedding_model"),
                    "metadata.zero_shot_tags": metadata_to_add["zero_shot_tags"]
                }}
            )
            print(f"Updated document {doc_id}. matched: {result.matched_count}, modified: {result.modified_count}")
        else:
            print(f"User chose not to update doc {doc_id}.")
            user_input2 = input("Do you want to retry for this document? (y/n): ").strip().lower()
            if user_input2 == "y":
                result = coll.update_one(
                    {"_id": doc_id},
                    {"$set": {
                        "metadata.image_embedding": metadata_to_add["image_embedding"],
                        "metadata.embedding_dim": metadata_to_add.get("embedding_dim"),
                        "metadata.embedding_model": metadata_to_add.get("embedding_model"),
                        "metadata.zero_shot_tags": metadata_to_add["zero_shot_tags"]
                    }}
                )
                print(f"Updated document {doc_id}. matched: {result.matched_count}, modified: {result.modified_count}")
            else:
                print(f"Skipping document {doc_id} permanently (user declined twice).")

    client.close()
    print("Done.")

if __name__ == "__main__":
    main()
