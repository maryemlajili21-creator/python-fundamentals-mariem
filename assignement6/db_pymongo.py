from pymongo import MongoClient
from pymongo.database import Database
from typing import Any


def get_client() -> MongoClient[Any]:
    """Connecting to local MongoDB (no Docker)."""
    return MongoClient("mongodb://localhost:27017/")


def get_db() -> Database[Any]:
    client = get_client()
    return client["users_db"]
