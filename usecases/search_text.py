from __future__ import annotations

from typing import List

from models.mongo import ScientificArticle


def search_text(keyword: str) -> List[ScientificArticle]:
    """Search in MongoDB using the text index on 'text' field."""
    query = ScientificArticle.objects.search_text(keyword)
    results = list(query)
    print(f"[MongoDB] Found {len(results)} article(s) for '{keyword}'")
    return results
