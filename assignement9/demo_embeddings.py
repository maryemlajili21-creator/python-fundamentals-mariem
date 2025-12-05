# demo_embeddings.py

from typing import List

import numpy as np
from config_gemini import get_embedding


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    Calcule la similarité cosinus entre deux vecteurs numériques.
    """
    va = np.array(a, dtype=float)
    vb = np.array(b, dtype=float)

    numerator = np.dot(va, vb)
    denominator = np.linalg.norm(va) * np.linalg.norm(vb)

    if denominator == 0:
        return 0.0

    return float(numerator / denominator)


if __name__ == "__main__":
    phrases = [
        "Quantum physics describes interactions between subatomic particles.",
        "Hadron experiments analyze collisions inside accelerators.",
        "Cooking recipes describe how to prepare meals.",
    ]

    print("Génération des embeddings...\n")

    embeddings = [get_embedding(p) for p in phrases]

    print(f"Dimension des vecteurs : {len(embeddings[0])}\n")

    sim_0_1 = cosine_similarity(embeddings[0], embeddings[1])
    sim_0_2 = cosine_similarity(embeddings[0], embeddings[2])

    print("Phrase A :", phrases[0])
    print("Phrase B :", phrases[1])
    print("Phrase C :", phrases[2])
    print()
    print(f"Similarité (A,B) : {sim_0_1:.4f}")
    print(f"Similarité (A,C) : {sim_0_2:.4f}")
