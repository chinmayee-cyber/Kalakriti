import json
from typing import Dict, Any, Optional
from models.data_models import PracticeTemplate

class TemplateService:
    """Service for generating art practice templates"""
    
    def __init__(self):
        self.template_library = self._load_template_library()
    
    async def generate_art_template(
        self, 
        style: str, 
        difficulty: str = "beginner"
    ) -> PracticeTemplate:
        """Generate practice template for art style"""
        
        base_template = self.template_library.get(style.lower(), {})
        difficulty_settings = self._get_difficulty_settings(difficulty)
        
        return PracticeTemplate(
            style=style,
            difficulty=difficulty,
            grid_layout=base_template.get("grid_layout", "5x5"),
            elements=self._get_elements_for_difficulty(
                base_template.get("elements", []),
                difficulty
            ),
            instructions=self._generate_instructions(style, difficulty),
            printable_url=self._generate_printable_url(style, difficulty)
        )
    
    def _load_template_library(self) -> Dict[str, Any]:
        """Load template library"""
        return {
            "warli": {
                "grid_layout": "6x6",
                "elements": [
                    {"type": "circle", "position": "center", "size": "medium"},
                    {"type": "triangle", "position": "border", "size": "small"},
                    {"type": "stick_figure", "position": "center", "size": "large"}
                ]
            },
            "madhubani": {
                "grid_layout": "8x8",
                "elements": [
                    {"type": "border_pattern", "position": "edge", "size": "full"},
                    {"type": "nature_element", "position": "center", "size": "medium"}
                ]
            }
        }