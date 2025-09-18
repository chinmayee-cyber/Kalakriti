from typing import List, Dict, Optional

def generate_caption(style_labels: List[str], subject_labels: List[str], medium: str) -> str:
    """
    Generate a caption based on style, subject, and medium
    
    Args:
        style_labels: List of style labels
        subject_labels: List of subject labels
        medium: Medium of the artwork
        
    Returns:
        Generated caption string
    """
    time_period = "contemporary"
    if any(style in ["Renaissance", "Baroque", "Classical"] for style in style_labels):
        time_period = "classical"
    elif any(style in ["Impressionism", "Realism"] for style in style_labels):
        time_period = "19th-20th century"
    
    primary_style = style_labels[0].lower() if style_labels else "artistic"
    primary_subject = subject_labels[0].lower() if subject_labels else "artwork"
    
    return f"A {time_period} {medium.lower()} {primary_subject} in {primary_style} style"

def create_metadata_dict(
    caption: str,
    style_labels: List[str],
    medium: str,
    dominant_colors: List[str],
    foreground_objects: List[str],
    background: str,
    aspect_ratio: str,
    image_embedding: List[float],
    texture: str,
    lighting: str
) -> Dict:
    """
    Create a metadata dictionary with standardized structure
    
    Args:
        caption: Generated caption
        style_labels: List of style labels
        medium: Medium of the artwork
        dominant_colors: List of dominant colors
        foreground_objects: List of foreground objects
        background: Background description
        aspect_ratio: Aspect ratio string
        image_embedding: CLIP image embedding
        texture: Texture description
        lighting: Lighting description
        
    Returns:
        Structured metadata dictionary
    """
    return {
        "caption": caption,
        "style_labels": style_labels,
        "medium_labels": [f"{medium} painting"],
        "dominant_colors": dominant_colors,
        "composition": {
            "foreground_objects": foreground_objects,
            "background": background,
            "aspect_ratio": aspect_ratio
        },
        "image_embedding": image_embedding,
        "texture": texture,
        "lighting": lighting
    }