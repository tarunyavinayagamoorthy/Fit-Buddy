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


def generate_nutrition_tip_with_flash(goal):

    prompt = f"""
You are FitBuddy's nutrition and recovery assistant.

The user's fitness goal is:

{goal}

Provide ONE concise and practical nutrition or recovery tip
that supports this fitness goal.

The advice should be simple, actionable and easy to understand.

Examples of areas you may consider:

- protein
- hydration
- balanced meals
- recovery
- post-workout nutrition

Do not provide a long meal plan.

Return only the useful tip.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text