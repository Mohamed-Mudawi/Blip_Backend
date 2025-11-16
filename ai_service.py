from groq import Groq
from config import GROQ_API_KEY
import json

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
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": messy_text}
        ],
        response_format={"type": "json_object"}
    )

    # Parse the JSON string from the response content
    return json.loads(response.choices[0].message.content)