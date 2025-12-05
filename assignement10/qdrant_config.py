# qdrant_config.py

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()


def get_qdrant_client() -> QdrantClient:
    """
    Crée un client Qdrant.
    - Si QDRANT_URL est défini: utilise Qdrant Cloud (HTTPS + API key)
    - Sinon: suppose un Qdrant local sur localhost:6333
    """
    url: Optional[str] = os.getenv("QDRANT_URL")
    api_key: Optional[str] = os.getenv("QDRANT_API_KEY")

    if url:
        if not api_key:
            raise ValueError(
                "QDRANT_URL est défini mais QDRANT_API_KEY manque dans .env"
            )
        return QdrantClient(url=url, api_key=api_key)

    # fallback: serveur local
    return QdrantClient(host="localhost", port=6333)
