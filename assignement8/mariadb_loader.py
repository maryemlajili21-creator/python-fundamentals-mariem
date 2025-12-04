import pandas as pd

from assignement8.models.relational import Author, ScientificArticle
from assignement8.storage.relational_db import Session


def insert_into_mariadb(df: pd.DataFrame) -> pd.DataFrame:
    """Insert each row of the DataFrame into MariaDB and return DataFrame with new IDs."""

    def save_row(row: pd.Series) -> pd.Series:
        with Session() as session:
            author = Author(
                full_name=row["author_full_name"],
                title=row["author_title"],
            )

            article = ScientificArticle(
                title=row["title"],
                summary=row["summary"],
                arxiv_id=row["arxiv_id"],
                file_path=row["file_path"],
                content=row["content"],
                author=author,
            )

            session.add(article)
            session.commit()

            return pd.Series(
                {"article_id": article.id, "author_id": author.id},
                index=["article_id", "author_id"],
            )

    ids = df.apply(save_row, axis=1)
    return pd.concat([df, ids], axis=1)
