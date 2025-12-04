from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection


def get_mongo_collection() -> Collection[Any]:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["arxiv_db"]
    return db["articles"]
