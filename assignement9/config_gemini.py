# config_gemini.py

import os
from typing import List

from dotenv import load_dotenv
from google import genai

print(">>> config_gemini chargé depuis :", __file__)

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Google GenAI client
client = genai.Client(api_key=api_key)


def get_embedding(text: str) -> List[float]:
    """
    Generating text embeddings using the correct signature for
    google-genai 1.53.0: embed_content(contents=[...]).
    """

    result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=[text],  # <-- THE ONLY VALID ARGUMENT FOR YOUR VERSION
    )

    if not result.embeddings:
        raise ValueError("No embeddings returned.")

    values = result.embeddings[0].values

    if values is None:
        raise ValueError("Embedding returned None.")

    return list(values)
