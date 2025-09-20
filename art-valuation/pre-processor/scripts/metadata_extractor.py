#!/usr/bin/env python3
"""
clip_embedding_and_tags.py

Minimal utilities to:
 - compute a CLIP image embedding (L2-normalized list of floats)
 - compute zero-shot label scores (top-k) given a list of candidate labels

Supports image sources that are either a URL or a local file path.

Dependencies:
    pip install torch torchvision ftfy regex tqdm
    pip install git+https://github.com/openai/CLIP.git
    pip install pillow requests numpy

Example:
    python clip_embedding_and_tags.py --image "https://example.com/img.jpg"
"""
from typing import List, Dict, Tuple
import os
import io
import argparse
import requests
from PIL import Image
import numpy as np
import torch
import clip


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

        # encode texts (batch)
        text_tokens = clip.tokenize(candidate_texts).to(self.device)  # N x token_len
        text_feat = self.model.encode_text(text_tokens)  # N x D
        text_feat = text_feat / text_feat.norm(dim=-1, keepdim=True)

        # similarity logits: scaled cosine (as CLIP does)
        logits = (100.0 * img_feat @ text_feat.T).cpu().numpy().squeeze(0)  # shape: (N,)

        # convert to probabilities via softmax (numerically stable)
        exps = np.exp(logits - np.max(logits))
        probs = exps / (np.sum(exps) + 1e-12)

        # select top_k
        idxs = np.argsort(-probs)[:min(top_k, len(candidate_texts))]
        return [{"label": candidate_texts[i], "score": float(probs[i])} for i in idxs]


def extract_embedding_and_tags(image_source: str, candidate_texts: List[str], top_k: int = 6,
                               model_name: str = "ViT-B/32", device: str = None
                              ) -> Dict:
    """High-level convenience wrapper."""
    img = load_image(image_source)
    clip_w = ClipWrapper(model_name=model_name, device=device)
    embedding = clip_w.get_image_embedding(img)  # numpy array
    tags = clip_w.zero_shot_scores(img, candidate_texts, top_k=top_k)
    return {
        "image_embedding": embedding.tolist(),
        "embedding_dim": int(embedding.shape[0]),
        "embedding_model": clip_w.model_name,
        "zero_shot_tags": tags
    }


# -------------------------
# Small default candidate list tuned for artwork metadata
# -------------------------
DEFAULT_CANDIDATES = [
    "landscape", "portrait", "seascape", "cityscape", "still life", "abstract",
    "figurative", "impressionist", "expressionist", "contemporary", "modern",
    "oil painting", "watercolor", "acrylic", "print", "photograph", "black and white",
    "colorful", "large", "small", "signed", "unsigned", "textured", "flat"
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract CLIP image embedding + zero-shot tags")
    parser.add_argument("--image", required=True, help="Image URL or local path")
    parser.add_argument("--top-k", type=int, default=6, help="Number of top zero-shot tags to return")
    parser.add_argument("--model", default="ViT-B/32", help="CLIP model name (e.g. ViT-B/32)")
    parser.add_argument("--device", default=None, help="torch device (e.g. 'cpu' or 'cuda'). Default auto-detect")
    args = parser.parse_args()

    print("Loading and processing image:", args.image)
    result = extract_embedding_and_tags(args.image, DEFAULT_CANDIDATES, top_k=args.top_k,
                                        model_name=args.model, device=args.device)

    print("\n--- Result ---")
    print("embedding_dim:", result["embedding_dim"])
    print("embedding_model:", result["embedding_model"])
    print("first 8 embedding values:", result["image_embedding"][:8])
    print("\nTop zero-shot tags:")
    for tag in result["zero_shot_tags"]:
        print(f" - {tag['label']}: {tag['score']:.4f}")
