import json
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import aiohttp
from google.adk import ModelConfig
from config import settings

@dataclass
class LessonContent:
    title: str
    overview: str
    historical_context: str
    key_characteristics: List[str]
    materials_needed: List[str]
    techniques: List[str]
    practice_steps: List[Dict[str, str]]
    common_mistakes: List[str]
    template_description: str
    quiz_questions: List[Dict[str, Any]]
    sources: List[Dict[str, str]]
    estimated_duration: str
    difficulty_level: str

class LessonGenerator:
    """Generates structured art lessons using LLM with RAG from search results"""
    
    def __init__(self, model_config: Optional[ModelConfig] = None):
        self.model_config = model_config or ModelConfig(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )
        self.prompt_templates = self._load_prompt_templates()
    
    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load prompt templates for different lesson types"""
        return {
            "basic_lesson": """
You are an expert art educator specializing in {style} art. Create a comprehensive lesson plan for a {level} student.

Style: {style}
Student Level: {level}
Student Interests: {interests}
Learning Goals: {goals}

Search Results Context:
{search_context}

Canonical Knowledge:
{canonical_context}

Generate a structured lesson plan with the following sections:
1. Title and Overview (brief introduction)
2. Historical Context (origin and cultural significance)
3. Key Characteristics (distinguishing features)
4. Materials Needed (traditional and modern alternatives)
5. Techniques (specific methods used in this style)
6. Practice Steps (3-5 progressive exercises with time estimates)
7. Common Mistakes to Avoid
8. Practice Template Description (for printable guide)
9. Quiz Questions (3-5 questions with multiple choice answers)
10. Recommended Resources (from search results)

Format the response as valid JSON with these keys:
- title
- overview
- historical_context
- key_characteristics (array)
- materials_needed (array)
- techniques (array)
- practice_steps (array of objects with "step", "description", "duration")
- common_mistakes (array)
- template_description
- quiz_questions (array of objects with "question", "options", "correct_answer")
- sources (array of objects with "title", "url")
- estimated_duration
- difficulty_level

Ensure the content is accurate, culturally respectful, and appropriate for the student's level.
"""
        }
    
    async def generate_lesson_content(
        self,
        style: str,
        search_context: str,
        canonical_context: Dict[str, Any],
        user_level: str = "beginner",
        user_interests: List[str] = None,
        learning_goals: List[str] = None
    ) -> LessonContent:
        """Generate structured lesson content using LLM"""
        
        # Prepare the prompt
        prompt = self.prompt_templates["basic_lesson"].format(
            style=style,
            level=user_level,
            interests=", ".join(user_interests) if user_interests else "Not specified",
            goals=", ".join(learning_goals) if learning_goals else "General learning",
            search_context=search_context,
            canonical_context=json.dumps(canonical_context, indent=2)
        )
        
        # Call the LLM (using ADK's model interface)
        try:
            # This assumes you have ADK set up with proper model configuration
            # Replace with your actual ADK model invocation
            response = await self._call_llm(prompt)
            
            # Parse the response
            lesson_data = self._parse_llm_response(response)
            
            # Create LessonContent object
            return LessonContent(
                title=lesson_data.get("title", f"Introduction to {style}"),
                overview=lesson_data.get("overview", ""),
                historical_context=lesson_data.get("historical_context", ""),
                key_characteristics=lesson_data.get("key_characteristics", []),
                materials_needed=lesson_data.get("materials_needed", []),
                techniques=lesson_data.get("techniques", []),
                practice_steps=lesson_data.get("practice_steps", []),
                common_mistakes=lesson_data.get("common_mistakes", []),
                template_description=lesson_data.get("template_description", ""),
                quiz_questions=lesson_data.get("quiz_questions", []),
                sources=lesson_data.get("sources", []),
                estimated_duration=lesson_data.get("estimated_duration", "1-2 hours"),
                difficulty_level=lesson_data.get("difficulty_level", user_level)
            )
            
        except Exception as e:
            # Fallback to a basic lesson structure if LLM fails
            return self._create_fallback_lesson(style, search_context, user_level)
    
    async def _call_llm(self, prompt: str) -> str:
        """Call the LLM using ADK's model interface"""
        # This is a placeholder for actual ADK model invocation
        # In practice, you would use: 
        # response = await self.model_config.model.generate(prompt)
        
        # For demonstration, we'll simulate a response
        # In production, replace with actual ADK code
        simulated_response = self._simulate_llm_response(prompt)
        return simulated_response
    
    def _simulate_llm_response(self, prompt: str) -> str:
        """Simulate an LLM response for demonstration purposes"""
        # Extract style from prompt
        style_match = re.search(r"Style: (\w+)", prompt)
        style = style_match.group(1) if style_match else "Art"
        
        # Extract level from prompt
        level_match = re.search(r"Student Level: (\w+)", prompt)
        level = level_match.group(1) if level_match else "beginner"
        
        # Return simulated JSON response
        return json.dumps({
            "title": f"Introduction to {style} Art",
            "overview": f"{style} art is characterized by its unique patterns and cultural significance. This lesson will introduce you to the basics.",
            "historical_context": f"{style} art originated in ancient times and has evolved to become a respected art form with deep cultural roots.",
            "key_characteristics": ["Geometric patterns", "Natural pigments", "Symbolic representations"],
            "materials_needed": ["Paper", "Pencils", "Natural pigments or alternatives"],
            "techniques": ["Line drawing", "Pattern repetition", "Color application"],
            "practice_steps": [
                {
                    "step": "1",
                    "description": "Practice basic shapes and patterns",
                    "duration": "15 minutes"
                },
                {
                    "step": "2",
                    "description": "Create a simple composition using these elements",
                    "duration": "30 minutes"
                },
                {
                    "step": "3",
                    "description": "Add color and details to your composition",
                    "duration": "45 minutes"
                }
            ],
            "common_mistakes": [
                "Using too many different patterns",
                "Not maintaining consistent line thickness",
                "Rushing the composition process"
            ],
            "template_description": f"A4 printable template with basic {style} patterns and guidelines",
            "quiz_questions": [
                {
                    "question": f"What is a key characteristic of {style} art?",
                    "options": ["Photorealism", "Geometric patterns", "Abstract expressionism"],
                    "correct_answer": "Geometric patterns"
                }
            ],
            "sources": [
                {
                    "title": f"Introduction to {style} Art",
                    "url": "https://example.com/intro"
                }
            ],
            "estimated_duration": "2 hours",
            "difficulty_level": level
        })
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse the LLM response and extract JSON content"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # If no JSON found, try to parse the whole response
                return json.loads(response)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a basic structure
            return {
                "title": "Art Lesson",
                "overview": "A comprehensive art lesson based on available resources.",
                "historical_context": "",
                "key_characteristics": [],
                "materials_needed": [],
                "techniques": [],
                "practice_steps": [],
                "common_mistakes": [],
                "template_description": "",
                "quiz_questions": [],
                "sources": [],
                "estimated_duration": "1-2 hours",
                "difficulty_level": "beginner"
            }
    
    def _create_fallback_lesson(
        self,
        style: str,
        search_context: str,
        user_level: str
    ) -> LessonContent:
        """Create a fallback lesson when LLM generation fails"""
        return LessonContent(
            title=f"Introduction to {style} Art",
            overview=f"Learn the basics of {style} art through guided practice.",
            historical_context=f"{style} art has a rich cultural history with unique characteristics.",
            key_characteristics=["Patterns", "Symbols", "Traditional techniques"],
            materials_needed=["Paper", "Pencil", "Coloring materials"],
            techniques=["Basic shapes", "Pattern repetition", "Composition"],
            practice_steps=[
                {
                    "step": "1",
                    "description": "Practice the basic elements of this style",
                    "duration": "20 minutes"
                },
                {
                    "step": "2",
                    "description": "Create a simple composition using these elements",
                    "duration": "30 minutes"
                },
                {
                    "step": "3",
                    "description": "Refine your work and add details",
                    "duration": "40 minutes"
                }
            ],
            common_mistakes=[
                "Rushing through the practice",
                "Not understanding the cultural context",
                "Using inappropriate materials"
            ],
            template_description=f"Basic practice template for {style} art",
            quiz_questions=[
                {
                    "question": f"What is a common characteristic of {style} art?",
                    "options": ["Realism", "Abstract patterns", "Geometric shapes"],
                    "correct_answer": "Geometric shapes"
                }
            ],
            sources=[{"title": "Online resources", "url": "https://example.com"}],
            estimated_duration="1.5 hours",
            difficulty_level=user_level
        )
    
    def generate_comparison_content(
        self,
        style1: str,
        style2: str,
        style1_data: Dict[str, Any],
        style2_data: Dict[str, Any],
        user_level: str
    ) -> Dict[str, Any]:
        """Generate content comparing two art styles"""
        
        similarities = []
        differences = []
        
        # Compare key characteristics
        chars1 = set(style1_data.get("key_characteristics", []))
        chars2 = set(style2_data.get("key_characteristics", []))
        
        similarities.extend(list(chars1.intersection(chars2)))
        differences.append({
            "aspect": "Key Characteristics",
            style1: list(chars1 - chars2),
            style2: list(chars2 - chars1)
        })
        
        # Compare materials
        materials1 = set(style1_data.get("materials_needed", []))
        materials2 = set(style2_data.get("materials_needed", []))
        
        similarities.extend(list(materials1.intersection(materials2)))
        differences.append({
            "aspect": "Materials",
            style1: list(materials1 - materials2),
            style2: list(materials2 - materials1)
        })
        
        # Determine which style is better for the user's level
        difficulty1 = style1_data.get("difficulty_level", "intermediate")
        difficulty2 = style2_data.get("difficulty_level", "intermediate")
        
        difficulty_map = {"beginner": 1, "intermediate": 2, "advanced": 3}
        diff1 = difficulty_map.get(difficulty1, 2)
        diff2 = difficulty_map.get(difficulty2, 2)
        
        if user_level == "beginner":
            recommended = style1 if diff1 <= diff2 else style2
        elif user_level == "advanced":
            recommended = style1 if diff1 >= diff2 else style2
        else:
            recommended = style1 if abs(diff1 - 2) <= abs(diff2 - 2) else style2
        
        return {
            "style1": style1,
            "style2": style2,
            "similarities": similarities,
            "differences": differences,
            "recommended_style": recommended,
            "reasoning": f"Recommended for {user_level} level based on complexity and required skills"
        }