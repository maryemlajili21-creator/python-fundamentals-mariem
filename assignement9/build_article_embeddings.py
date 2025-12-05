from __future__ import annotations

import json
import os
from typing import List

import pandas as pd
from config_gemini import get_embedding
from tqdm import tqdm


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if end < len(text):
            index_last_period = chunk.rfind(".")
            if index_last_period > chunk_size // 2:
                end = start + index_last_period + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())

        start = end - overlap

    return chunks


def load_articles(csv_path: str) -> pd.DataFrame:
    """
    Charge les articles depuis un fichier CSV.
    Le fichier doit contenir au minimum : article_id, title, text.
    """

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Fichier introuvable : {csv_path}")

    df = pd.read_csv(csv_path)

    expected_cols = {"article_id", "title", "text"}
    missing_cols = expected_cols - set(df.columns)

    if missing_cols:
        raise ValueError(f"Colonnes manquantes dans CSV : {missing_cols}")

    return df


def build_chunks_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforme un DataFrame d'articles en un DataFrame où chaque ligne est un chunk.
    """

    rows = []

    for _, row in df.iterrows():
        article_id = row["article_id"]
        title = row["title"]
        full_text = row["text"]

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


def add_embeddings(chunks_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute une colonne 'embedding' contenant un vecteur pour chaque chunk.
    """

    embeddings = []

    for _, row in tqdm(chunks_df.iterrows(), total=len(chunks_df)):
        text = row["chunk_text"]
        emb = get_embedding(text)
        embeddings.append(emb)

    chunks_df = chunks_df.copy()
    chunks_df["embedding"] = embeddings

    return chunks_df


def save_jsonl(df: pd.DataFrame, output_path: str) -> None:
    """
    Sauvegarde un DataFrame dans un fichier JSON Lines (JSONL),
    où chaque ligne représente un chunk + embedding.
    """

    with open(output_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            record = {
                "article_id": row["article_id"],
                "title": row["title"],
                "chunk_index": int(row["chunk_index"]),
                "chunk_text": row["chunk_text"],
                "embedding": row["embedding"],
            }
            f.write(json.dumps(record) + "\n")


def main() -> None:
    csv_path = "articles.csv"
    output_path = "article_chunks_embeddings.jsonl"

    print("\n--- Chargement des articles ---")
    df = load_articles(csv_path)
    print(f"{len(df)} articles chargés.\n")

    print("--- Création des chunks ---")
    chunks_df = build_chunks_dataframe(df)
    print(f"{len(chunks_df)} chunks générés.\n")

    print("--- Génération des embeddings pour chaque chunk ---")
    chunks_df = add_embeddings(chunks_df)

    print(f"\n--- Sauvegarde dans {output_path} ---")
    save_jsonl(chunks_df, output_path)

    print("\nPipeline terminé avec succès !\n")


if __name__ == "__main__":
    main()
