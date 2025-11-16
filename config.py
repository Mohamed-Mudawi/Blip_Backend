# /backend/config.py

import os
from dotenv import load_dotenv

# Load .env ONLY locally — safe on Render too
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("The GROQ_API_KEY environment variable is not set.")
