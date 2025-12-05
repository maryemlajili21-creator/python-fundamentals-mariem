# qdrant_pipeline.py

from __future__ import annotations

import os
from typing import List

import pandas as pd
from config_gemini import get_embedding
from models_qdrant import ArticleChunkPayload
from qdrant_client.models import Distance, PointStruct, VectorParams
from qdrant_config import get_qdrant_client
from tqdm import tqdm

COLLECTION_NAME = "article_chunks"


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Découpe un texte long en segments (chunks) avec chevauchement.
    """
    if not text:
        return []

    chunks: List[str] = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if end < len(text):
            last_period = chunk.rfind(".")
            if last_period > chunk_size // 2:
                end = start + last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks


def load_articles(csv_path: str) -> pd.DataFrame:
    """
    Charge les articles depuis un CSV avec colonnes:
    article_id, title, text
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Fichier introuvable : {csv_path}")

    df = pd.read_csv(csv_path)
    expected_cols = {"article_id", "title", "text"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Colonnes manquantes dans CSV : {missing}")
    return df


def build_chunks_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforme un DataFrame d'articles en un DataFrame de chunks.
    """
    rows: List[dict] = []

    for _, row in df.iterrows():
        article_id = int(row["article_id"])
        title = str(row["title"])
        full_text = str(row["text"])

        chunks = chunk_text(full_text, chunk_size=1000, overlap=200)

        for idx, chunk in enumerate(chunks):
            rows.append(
                {
                    "article_id": article_id,
                    "title": title,
                    "chunk_index": idx,
                    "chunk_text": chunk,
                }
            )

    return pd.DataFrame(rows)


def ensure_collection() -> None:
    """
    Crée la collection Qdrant si elle n'existe pas.
    On suppose des embeddings de dimension 768 (text-embedding-004).
    """
    client = get_qdrant_client()

    collections = client.get_collections()
    existing = {c.name for c in collections.collections}
    if COLLECTION_NAME in existing:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE,
        ),
    )


def make_point_id(article_id: int, chunk_index: int) -> int:
    """
    Construit un ID déterministe pour le chunk, à partir de (article_id, chunk_index).
    """
    return abs(hash((article_id, chunk_index))) % (2**63)


def chunk_exists(point_id: int) -> bool:
    """
    Vérifie si un chunk avec ce point_id existe déjà dans Qdrant.
    """
    client = get_qdrant_client()
    points = client.retrieve(
        collection_name=COLLECTION_NAME,
        ids=[point_id],
    )
    return len(points) > 0


def insert_chunk(payload: ArticleChunkPayload, embedding: List[float]) -> None:
    """
    Insère un chunk dans Qdrant avec son embedding.
    """
    client = get_qdrant_client()
    point_id = make_point_id(payload.article_id, payload.chunk_index)

    point = PointStruct(
        id=point_id,
        vector=embedding,
        payload=payload.model_dump(),
    )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point],
    )


def process_articles_to_qdrant(csv_path: str = "articles.csv") -> None:
    """
    Pipeline complet:
    - charge les articles
    - explose en chunks
    - crée la collection Qdrant
    - pour chaque chunk:
        - skip si déjà en DB
        - sinon: calcule embedding + insert
    """

    df = load_articles(csv_path)
    print(f"{len(df)} articles charged.\n")

    chunks_df = build_chunks_dataframe(df)
    print(f"{len(chunks_df)} chunks generated.\n")

    ensure_collection()

    print(" insert chunks in Qdrant (with embeddings) ")

    for _, row in tqdm(chunks_df.iterrows(), total=len(chunks_df)):
        article_id = int(row["article_id"])
        title = str(row["title"])
        chunk_index = int(row["chunk_index"])
        chunk_text = str(row["chunk_text"])

        point_id = make_point_id(article_id, chunk_index)
        if chunk_exists(point_id):
            # chunk déjà présent: ne recalcule pas l'embedding
            continue

        # calcule l'embedding uniquement pour les chunks manquants
        embedding = get_embedding(chunk_text)

        payload = ArticleChunkPayload(
            article_id=article_id,
            title=title,
            chunk_index=chunk_index,
            chunk_text=chunk_text,
        )
        insert_chunk(payload, embedding)


if __name__ == "__main__":
    process_articles_to_qdrant()
