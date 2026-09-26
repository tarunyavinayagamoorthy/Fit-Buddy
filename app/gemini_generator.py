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


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):
    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a personalized 7-day workout plan.

User information:
Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

Generate a structured plan for Day 1 through Day 7.

For each day include:

1. Day
2. Workout focus
3. Warm-up (5-10 minutes)
4. Main workout
5. Exercise name
6. Sets and repetitions OR duration
7. Rest interval
8. Cool-down/recovery guidance

The plan should be appropriate for the selected goal
and workout intensity.

Keep the response structured and easy to read.

Do not include unnecessary introductory text.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text