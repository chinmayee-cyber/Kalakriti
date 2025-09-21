from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class LessonPlan:
    title: str
    overview: str
    historical_context: str
    key_characteristics: List[str]
    materials_needed: List[str]
    practice_steps: List[Dict[str, str]]
    template_description: str
    quiz_questions: List[Dict[str, Any]]
    sources: List[Dict[str, str]]
    estimated_duration: str
    difficulty_level: str

@dataclass
class ArtStyleComparison:
    style1: str
    style2: str
    similarities: List[str]
    differences: List[Dict[str, Any]]
    recommended_style: str
    reasoning: str

@dataclass
class PracticeTemplate:
    style: str
    difficulty: str
    grid_layout: str
    elements: List[Dict[str, Any]]
    instructions: str
    printable_url: Optional[str] = None