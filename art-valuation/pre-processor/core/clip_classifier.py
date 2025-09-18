import torch
import clip
from PIL import Image
from typing import List, Dict
import numpy as np
from config.settings import Config

class CLIPClassifier:
    """Optimized CLIP classification with caching"""
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = None, None
        self.text_embeddings = {}
        self._load_model()
        self._precompute_text_embeddings()
    
    def _load_model(self):
        """Load CLIP model and set to evaluation mode"""
        print(f"Loading CLIP model on {self.device}")
        self.model, self.preprocess = clip.load(Config.CLIP_MODEL, device=self.device)
        self.model.eval()  # Set to eval mode for inference
    
    def _get_style_labels(self) -> List[str]:
        """Get style labels from configuration"""
        return Config.STYLE_LABELS.split(',')
    
    def _get_subject_labels(self) -> List[str]:
        """Get subject labels from configuration"""
        return Config.SUBJECT_LABELS.split(',')
    
    def _get_composition_objects(self) -> List[str]:
        """Get composition objects from configuration"""
        return Config.COMPOSITION_OBJECTS.split(',')
    
    def _get_lighting_conditions(self) -> List[str]:
        """Get lighting conditions from configuration"""
        return Config.LIGHTING_CONDITIONS.split(',')
    
    def _get_texture_descriptions(self) -> List[str]:
        """Get texture descriptions from configuration"""
        return Config.TEXTURE_DESCRIPTIONS.split(',')
    
    def _get_background_labels(self) -> List[str]:
        """Get background labels from configuration"""
        return Config.BACKGROUND_LABELS.split(',')
    
    def _precompute_text_embeddings(self):
        """Precompute all text embeddings for faster inference"""
        all_labels = {
            'style': self._get_style_labels(),
            'subject': self._get_subject_labels(),
            'objects': self._get_composition_objects(),
            'lighting': self._get_lighting_conditions(),
            'texture': self._get_texture_descriptions(),
            'background': self._get_background_labels()
        }
        
        for category, labels in all_labels.items():
            text_inputs = clip.tokenize(labels).to(self.device)
            with torch.no_grad():
                text_features = self.model.encode_text(text_inputs)
                text_features /= text_features.norm(dim=-1, keepdim=True)
                self.text_embeddings[category] = text_features
    
    @torch.no_grad()
    def get_image_embedding(self, image: Image.Image) -> List[float]:
        """
        Generate CLIP embedding for the image
        
        Args:
            image: PIL Image to process
            
        Returns:
            List of embedding values
        """
        from core.image_processor import ImageProcessor
        image = ImageProcessor.resize_image_for_clip(image)
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        
        image_features = self.model.encode_image(image_input)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        
        return image_features.cpu().numpy().flatten().tolist()
    
    @torch.no_grad()
    def classify_fast(self, image: Image.Image, category: str, top_k: int = 3) -> List[str]:
        """
        Fast classification using precomputed text embeddings
        
        Args:
            image: PIL Image to classify
            category: Category to classify (style, subject, etc.)
            top_k: Number of top results to return
            
        Returns:
            List of classification labels
        """
        from core.image_processor import ImageProcessor
        image = ImageProcessor.resize_image_for_clip(image)
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        
        image_features = self.model.encode_image(image_input)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        
        # Use precomputed text embeddings
        text_features = self.text_embeddings[category]
        
        similarities = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        top_probs, top_indices = similarities[0].topk(top_k)
        
        # Get the appropriate labels list based on category
        labels_method = getattr(self, f"_get_{category}_labels")
        labels_list = labels_method()
        
        result = []
        
        for i, prob in zip(top_indices, top_probs):
            if prob > Config.CONFIDENCE_THRESHOLD:
                result.append(labels_list[i])
        
        return result[:top_k] if result else [labels_list[top_indices[0]]]