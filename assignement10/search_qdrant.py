# search_qdrant.py

from __future__ import annotations

from typing import Any, List

from config_gemini import get_embedding
from qdrant_client import QdrantClient
from qdrant_config import get_qdrant_client
from qdrant_pipeline import COLLECTION_NAME


def search_chunks(query: str, limit: int = 5) -> List[dict[str, Any]]:
    """
    Convert the user query to an embedding and search Qdrant for the most similar chunks.
    """
    client: QdrantClient = get_qdrant_client()
    query_vector = get_embedding(query)

    # Modern Qdrant search API
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit,
        with_payload=True,
    )

    output: List[dict[str, Any]] = []
    for r in results:
        output.append(
            {
                "score": r.score,
                "article_id": r.payload.get("article_id"),
                "title": r.payload.get("title"),
                "chunk_index": r.payload.get("chunk_index"),
                "chunk_text": r.payload.get("chunk_text"),
            }
        )
    return output


if __name__ == "__main__":
    while True:
        query = input("Enter search query: ").strip()
        if query.lower() in ("quit", "exit"):
            break

        hits = search_chunks(query, limit=3)
        print("\nTop results:\n")
        for h in hits:
            print(f"[score={h['score']:.3f}] {h['title']}")
            print(h["chunk_text"][:200], "...\n")
