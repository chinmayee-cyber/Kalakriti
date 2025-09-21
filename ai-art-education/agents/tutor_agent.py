import json
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from tools.search_tool import TavilySearchTool
from agents.lesson_generator import LessonGenerator, LessonContent
from models.data_models import LessonPlan, ArtStyleComparison
from services.template_service import TemplateService

@dataclass
class UserContext:
    level: str = "beginner"
    interests: List[str] = None
    previous_styles: List[str] = None
    learning_goals: List[str] = None
    
    def __post_init__(self):
        if self.interests is None:
            self.interests = []
        if self.previous_styles is None:
            self.previous_styles = []
        if self.learning_goals is None:
            self.learning_goals = []

class TeachStyleAgent:
    """Enhanced art teaching agent with new features"""
    
    def __init__(self):
        self.search_tool = TavilySearchTool()
        self.template_service = TemplateService()
        self.lesson_generator = LessonGenerator()  # Add this line
        self.canonical_lessons = self._load_canonical_lessons()
    
    # Update the generate_lesson_plan method
    async def generate_lesson_plan(
        self,
        style_query: str,
        user_context: UserContext
    ) -> LessonContent:  # Change return type
        """Generate comprehensive lesson plan"""
        # Search for current information
        search_results = await self.search_tool.search_art_style(style_query)
        
        # Get canonical knowledge if available
        canonical_data = self.canonical_lessons.get(style_query.lower(), {})
        
        # Prepare search context
        search_context = self._prepare_search_context(search_results)
        
        # Generate lesson content using the lesson generator
        lesson_content = await self.lesson_generator.generate_lesson_content(
            style=style_query,
            search_context=search_context,
            canonical_context=canonical_data,
            user_level=user_context.level,
            user_interests=user_context.interests,
            learning_goals=user_context.learning_goals
        )
        
        return lesson_content
    
    def _prepare_search_context(self, search_results: List[Dict]) -> str:
        """Prepare search results as context for LLM"""
        context_parts = []
        for i, result in enumerate(search_results[:5]):  # Use top 5 results
            context_parts.append(
                f"Source {i+1}: {result.get('title', 'Unknown')}\n"
                f"Content: {result.get('snippet', 'No content available')}\n"
                f"URL: {result.get('url', 'No URL')}\n"
            )
        return "\n".join(context_parts)
    
    # Update the compare_art_styles method to use lesson generator
    async def compare_art_styles(
        self,
        style1: str,
        style2: str,
        user_context: UserContext
    ) -> Dict[str, Any]:
        """Compare two art styles"""
        # Get data for both styles
        results1 = await self.search_tool.search_art_style(style1)
        results2 = await self.search_tool.search_art_style(style2)
        
        canonical1 = self.canonical_lessons.get(style1.lower(), {})
        canonical2 = self.canonical_lessons.get(style2.lower(), {})
        
        # Generate lesson content for both styles to get structured data
        search_context1 = self._prepare_search_context(results1)
        search_context2 = self._prepare_search_context(results2)
        
        lesson1 = await self.lesson_generator.generate_lesson_content(
            style1, search_context1, canonical1, user_context.level
        )
        lesson2 = await self.lesson_generator.generate_lesson_content(
            style2, search_context2, canonical2, user_context.level
        )
        
        # Convert lessons to dict for comparison
        lesson1_dict = {
            "key_characteristics": lesson1.key_characteristics,
            "materials_needed": lesson1.materials_needed,
            "difficulty_level": lesson1.difficulty_level
        }
        
        lesson2_dict = {
            "key_characteristics": lesson2.key_characteristics,
            "materials_needed": lesson2.materials_needed,
            "difficulty_level": lesson2.difficulty_level
        }
        
        # Generate comparison
        comparison = self.lesson_generator.generate_comparison_content(
            style1, style2, lesson1_dict, lesson2_dict, user_context.level
        )
        
        return comparison