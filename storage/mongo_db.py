from __future__ import annotations

from mongoengine import connect


def init_mongo() -> None:
    """Connect to local MongoDB."""
    connect(
        db="articles_db",
        host="localhost",
        port=27017,
    )
