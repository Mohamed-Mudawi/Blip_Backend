# ai_service.py

from groq import Groq, APIError
from config import GROQ_API_KEY
import json

# Ensure the API key is present
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment or config.py")

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You take a messy event description from a user and output structured JSON 
to auto-fill a social media post form. Do NOT include explanations, only return JSON.

JSON FORMAT:
{
    "postContent": "string",
    "platforms": ["instagram", "twitter", "facebook", "linkedin"],
    "media": []
}

Rules:
- Create clean, engaging social media text.
- Keep platform character limits in mind.
- Always respond with JSON only.
"""

def generate_social_post(messy_text: str):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # UPDATED MODEL
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": messy_text}
            ],
            response_format={"type": "json_object"}
        )

        # Raw JSON string from Groq
        json_content = response.choices[0].message.content
        
        # Convert JSON string → Python dictionary
        return json.loads(json_content)

    except APIError as e:
        print(f"Groq API Call Failed: {e}")
        raise

    except json.JSONDecodeError as e:
        print(f"JSON Parsing Failed: {e}")
        print(f"Raw Groq Output: {json_content}")
        raise
