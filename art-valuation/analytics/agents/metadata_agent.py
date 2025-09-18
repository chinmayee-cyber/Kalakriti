"""
Metadata Agent
- Extracts metadata for an artwork from its image URL and existing metadata.
- Uses your existing art_meta.clip_classifier and image_processor modules.
"""

from google.adk.agents import Agent, Tool
from art_meta.config import Config
from art_meta.clip_classifier import CLIPClassifier
from art_meta.image_processor import ImageProcessor
from pymongo import MongoClient
from PIL import Image
from io import BytesIO
import requests
import numpy as np
import logging

logger = logging.getLogger(__name__)

class MetadataAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = MongoClient(Config.MONGO_URI)
        self.collection = self.client[Config.DB_NAME][Config.COLLECTION_NAME]
        self.classifier = CLIPClassifier()

    @Tool(name="generate_metadata", description="Generate metadata for artwork given _id")
    def generate_metadata(self, artwork_id: str) -> dict:
        """
        Fetches the document for artwork_id, downloads the image,
        computes metadata (caption, style_labels, medium_labels, dominant_colors, composition, embedding, texture, lighting),
        and updates the document in MongoDB with metadata field.
        Returns the metadata or error info.
        """
        doc = self.collection.find_one({"_id": artwork_id})
        if not doc:
            return {"ok": False, "error": "document not found"}

        img_url = doc.get("img_url")
        if not img_url:
            return {"ok": False, "error": "img_url missing"}

        try:
            resp = requests.get(img_url, timeout=Config.REQUEST_TIMEOUT)
            resp.raise_for_status()
            image = Image.open(BytesIO(resp.content)).convert("RGB")
            image = ImageProcessor.resize_image_for_clip(image)

            # Classification
            style_labels = self.classifier.classify_fast(image, "style", 2)
            subject_labels = self.classifier.classify_fast(image, "subject", 2)
            objects = self.classifier.classify_fast(image, "objects", 3)
            lighting = self.classifier.classify_fast(image, "lighting", 1)[0]
            texture = self.classifier.classify_fast(image, "texture", 1)[0]

            # Dominant colors
            arr = np.array(image).reshape(-1, 3)
            img_hash = hash(arr.tobytes())
            dominant_colors = list(ImageProcessor.get_dominant_colors_fast(img_hash, arr.tobytes()))

            # Embedding
            image_embedding = self.classifier.get_image_embedding(image)

            # Caption (reuse logic)
            time_period = "contemporary"
            if any(s in ["Renaissance", "Baroque", "Classical"] for s in style_labels):
                time_period = "classical"
            elif any(s in ["Impressionism", "Realism"] for s in style_labels):
                time_period = "19th-20th century"

            primary_style = style_labels[0].lower() if style_labels else "artistic"
            primary_subject = subject_labels[0].lower() if subject_labels else "artwork"
            medium_text = doc.get("medium", "painting").lower()

            caption = f"A {time_period} {medium_text} {primary_subject} in {primary_style} style"

            # Aspect ratio
            width, height = image.size
            if width >= height:
                aspect_ratio = f"{round(width / height, 1)}:1"
            else:
                aspect_ratio = f"1:{round(height / width, 1)}"

            metadata = {
                "caption": caption,
                "style_labels": style_labels,
                "medium_labels": [f"{doc.get('medium','Unknown')} painting"],
                "dominant_colors": dominant_colors,
                "composition": {
                    "foreground_objects": objects,
                    "background": None,
                    "aspect_ratio": aspect_ratio
                },
                "image_embedding": image_embedding,
                "texture": texture,
                "lighting": lighting
            }

            # Update MongoDB
            self.collection.update_one({"_id": artwork_id}, {"$set": {"metadata": metadata}})

            return {"ok": True, "metadata": metadata}

        except Exception as e:
            logger.exception(f"generate_metadata failed for {artwork_id}")
            return {"ok": False, "error": str(e)}
