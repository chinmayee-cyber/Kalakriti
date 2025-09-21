from google.adk.agents import SequentialAgent
from ai_art_education.agents.lesson_generator_agent import lesson_agent
from ai_art_education.agents.tutor_agent import tutor_agent

# Define main pipeline agent
main_pipeline = SequentialAgent(
    name="art_education_pipeline",
    sub_agents=[
        # Step 1: Generate raw lesson
        lesson_agent,

        # Step 2: Tutor agent refines / compares using lesson data
        tutor_agent
    ]
)