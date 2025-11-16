# ai_service.py

from groq import Groq
from groq import APIError  # <-- FIX 1: Import Groq's specific error class
from config import GROQ_API_KEY
import json

# Ensure the API key is not None before client creation (optional, but safer)
if not GROQ_API_KEY:
    # If the key is missing, raise an error immediately.
    # This will prevent silent failures and make the 500 error more traceable to the key.
    raise ValueError("GROQ_API_KEY is not set in environment or config.py")

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
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": messy_text}
            ],
            response_format={"type": "json_object"}
        )
        
        # Get the raw content from the model
        json_content = response.choices[0].message.content

        # Parse the JSON string from the response content
        return json.loads(json_content)
        
    except APIError as e:
        # FIX 2: Handle Groq API errors (like invalid key, rate limits, or bad requests)
        print(f"Groq API Call Failed: {e}")
        # Re-raise the exception to be caught by the app.py handler (which returns the 500)
        raise

    except json.JSONDecodeError as e:
        # FIX 3: Handle cases where the model returns malformed JSON
        print(f"JSON Parsing Failed: Model did not return valid JSON. Error: {e}")
        # Print the problematic raw content for debugging
        print(f"Raw Groq Output: {json_content}")
        raise