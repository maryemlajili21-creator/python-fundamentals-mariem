from __future__ import annotations

from pathlib import Path

from storage.relational_db import init_db
from storage.mongo_db import init_mongo
from usecases.import_articles import load_data_from_csv
from usecases.export_articles import export_from_mariadb_to_mongo
from usecases.search_text import search_text


def main() -> None:
    print("Initializing MariaDB...")
    init_db()

    print("Initializing MongoDB...")
    init_mongo()

    print("Loading data from CSV into MariaDB...")
    csv_path = Path("data") / "articles.csv"
    imported = load_data_from_csv(csv_path)
    print(f"Imported {len(imported)} article(s) into MariaDB.")

    print("Exporting data from MariaDB to MongoDB...")
    mongo_articles = export_from_mariadb_to_mongo()
    print(f"Exported {len(mongo_articles)} article(s) to MongoDB.")

    print("Running text search in MongoDB...")
    keyword = "network"

    results = search_text(keyword)

    print("Search results:")
    for article in results:
        print(f"- {article.arxiv_id}: {article.title}")


if __name__ == "__main__":
    main()
