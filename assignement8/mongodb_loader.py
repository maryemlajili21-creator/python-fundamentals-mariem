import pandas as pd

from assignement8.storage.mongo import get_mongo_collection


def export_to_mongodb(df: pd.DataFrame) -> pd.DataFrame:
    """Insert processed data into MongoDB."""

    collection = get_mongo_collection()

    def save_mongo(row: pd.Series) -> None:
        document = {
            "article_id": int(row["article_id"]),
            "author_id": int(row["author_id"]),
            "title": row["title"],
            "summary": row["summary"],
            "text": row["content"],
        }
        collection.insert_one(document)

    df.apply(save_mongo, axis=1)
    return df
