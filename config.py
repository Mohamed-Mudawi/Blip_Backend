# /backend/config.py

import os
# Do NOT load_dotenv() if you are on Render. It gets the variables directly from the OS.

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Keep the check to ensure the key is present, whether from Render or local .env (if you added load_dotenv() locally)
if GROQ_API_KEY is None:
    # On Render, this means you forgot to set the variable in the Dashboard!
    raise ValueError("The GROQ_API_KEY environment variable is not set.")