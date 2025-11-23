from __future__ import annotations

from typing import List

import pymupdf4llm
from mongoengine import DoesNotExist
from sqlalchemy import select

from models.mongo import Author as MongoAuthor
from models.mongo import ScientificArticle as MongoArticle
from models.relational import ScientificArticle
from storage.relational_db import get_session


def convert_pdf_to_markdown(file_path: str) -> str:
    """Convert a PDF file to Markdown."""
    return pymupdf4llm.to_markdown(file_path)


def export_from_mariadb_to_mongo() -> List[MongoArticle]:
    """Export all articles from MariaDB to MongoDB."""
    session = get_session()
    mongo_articles: List[MongoArticle] = []

    try:
        stmt = select(ScientificArticle).order_by(ScientificArticle.id)
        for article in session.scalars(stmt):
            # Convert PDF → Markdown
            md_text = convert_pdf_to_markdown(article.file_path)

            # Create embedded author for MongoDB
            m_author = MongoAuthor(
                db_id=article.author.id,
                full_name=article.author.full_name,
                title=article.author.title,
            )

            data = dict(
                db_id=article.id,
                title=article.title,
                summary=article.summary,
                file_path=article.file_path,
                arxiv_id=article.arxiv_id,
                created_at=article.created_at,
                author=m_author,
                text=md_text,
            )

            # Update if exists, else insert
            try:
                m_article = MongoArticle.objects.get(arxiv_id=article.arxiv_id)
                m_article.update(**data)
                m_article.reload()
                print(f"[MongoDB] Updated {article.arxiv_id}")

            except DoesNotExist:
                m_article = MongoArticle(**data)
                m_article.save()
                print(f"[MongoDB] Inserted {article.arxiv_id}")

            mongo_articles.append(m_article)

    finally:
        session.close()

    return mongo_articles
