# config_gemini.py

import os

from dotenv import load_dotenv
from google import genai

print(">>> config_gemini loaded from:", __file__)

# Load the .env file (GOOGLE_API_KEY must be inside)
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Initialize Gemini Client
client = genai.Client(api_key=api_key)


def get_embedding(text: str) -> list[float]:
    """
    Returns a vector embedding for the given text.
    Uses google-genai 1.53.0 embed_content() method.
    """
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
    )

    # result.embeddings is a list of embeddings; we want the first
    return result.embeddings[0].values
