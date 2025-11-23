from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd
from sqlalchemy.exc import IntegrityError

from models.relational import Author, ScientificArticle
from storage.relational_db import get_session


def load_data_from_csv(csv_path: Path) -> List[ScientificArticle]:
    """Read CSV with pandas and insert articles into MariaDB."""
    df = pd.read_csv(csv_path, sep=";")

    imported: List[ScientificArticle] = []

    for _, row in df.iterrows():
        session = get_session()
        try:
            author = Author(
                full_name=str(row["author_full_name"]),
                title=str(row["author_title"]),
            )
            article = ScientificArticle(
                title=str(row["title"]),
                summary=str(row["summary"]),
                file_path=str(row["file_path"]),
                arxiv_id=str(row["arxiv_id"]),
                author=author,
            )
            session.add(article)
            session.commit()
            imported.append(article)
            print(f"[MariaDB] Inserted {article.arxiv_id}")
        except IntegrityError:
            session.rollback()
            print(f"[MariaDB] Duplicate arxiv_id, skipping {row['arxiv_id']}")
        finally:
            session.close()

    return imported
