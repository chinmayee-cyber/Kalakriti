import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from config import settings
from agents.teach_agent import TeachStyleAgent, UserContext
from models.data_models import LessonPlan, ArtStyleComparison

app = FastAPI(title="Art Education Agent")
teach_agent = TeachStyleAgent()

class LessonRequest(BaseModel):
    style: str
    level: str = "beginner"
    interests: Optional[List[str]] = None
    learning_goals: Optional[List[str]] = None

class ComparisonRequest(BaseModel):
    style1: str
    style2: str
    user_level: str = "beginner"

@app.post("/lesson", response_model=LessonPlan)
async def generate_lesson(request: LessonRequest):
    """Generate art lesson endpoint"""
    try:
        user_context = UserContext(
            level=request.level,
            interests=request.interests or [],
            learning_goals=request.learning_goals or []
        )
        
        lesson = await teach_agent.generate_lesson_plan(
            request.style, 
            user_context
        )
        return lesson
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare", response_model=ArtStyleComparison)
async def compare_styles(request: ComparisonRequest):
    """Compare art styles endpoint"""
    try:
        user_context = UserContext(level=request.user_level)
        
        comparison = await teach_agent.compare_art_styles(
            request.style1,
            request.style2,
            user_context
        )
        return comparison
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/learning-path")
async def get_learning_path(level: str = "beginner", interests: List[str] = []):
    """Get personalized learning path"""
    try:
        user_context = UserContext(level=level, interests=interests)
        path = await teach_agent.generate_personalized_path(user_context)
        return {"learning_path": path}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)