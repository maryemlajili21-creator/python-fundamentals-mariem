# models_qdrant.py

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ArticleChunkPayload(BaseModel):
    """
    Metadata stored in Qdrant payload for each chunk.
    """

    article_id: int
    title: str
    chunk_index: int
    chunk_text: str

    # Optional metadata fields (if you want to extend later)
    author: Optional[str] = None
    arxiv_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
