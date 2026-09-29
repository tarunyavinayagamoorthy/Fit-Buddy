import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured in the .env file."
    )


client = genai.Client(api_key=API_KEY)


def update_workout_plan(
    original_plan,
    feedback,
    username,
    goal,
    intensity
):

    prompt = f"""
You are FitBuddy's workout plan updating assistant.

User:
Name: {username}
Goal: {goal}
Intensity: {intensity}

Original workout plan:

{original_plan}

User feedback:

{feedback}

Modify the original 7-day workout plan according
to the user's feedback.

Requirements:

- Preserve useful parts of the original plan.
- Apply the requested changes.
- Keep the plan suitable for the user's fitness goal.
- Maintain the same 7-day structure.
- Include warm-up.
- Include main workout.
- Include sets/repetitions or duration.
- Include rest intervals.
- Include cool-down/recovery guidance.

Return ONLY the revised workout plan.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text