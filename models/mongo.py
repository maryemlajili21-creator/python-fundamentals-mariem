from __future__ import annotations

from datetime import datetime

from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    IntField,
    StringField,
)


class Author(EmbeddedDocument):
    db_id = IntField(required=True)  # id from MariaDB
    full_name = StringField(required=True)
    title = StringField(required=True)


class ScientificArticle(Document):
    meta = {
        "collection": "articles",
        "indexes": [
            "db_id",
            "arxiv_id",
            {"fields": ["$text"]},  # text index on the "text" field
        ],
    }

    db_id = IntField(required=True)
    title = StringField(required=True)
    summary = StringField(required=True)
    file_path = StringField(required=True)
    arxiv_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    author = EmbeddedDocumentField(Author, required=True)
    text = StringField(required=True)  # PDF content converted to Markdown
