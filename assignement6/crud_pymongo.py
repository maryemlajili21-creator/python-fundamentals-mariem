from typing import TypedDict, Optional, List
from bson import ObjectId
from db_pymongo import get_db


class ProfileDict(TypedDict):
    age: int
    city: str


class UserDict(TypedDict, total=False):
    _id: ObjectId
    username: str
    email: str
    profile: ProfileDict


def create_user_pymongo(username: str, email: str, age: int, city: str) -> str:
    db = get_db()
    users = db["users"]

    doc: UserDict = {
        "username": username,
        "email": email,
        "profile": {"age": age, "city": city},
    }
    result = users.insert_one(doc)
    return str(result.inserted_id)


def get_user_by_id_pymongo(user_id: str) -> Optional[UserDict]:
    db = get_db()
    users = db["users"]
    try:
        oid = ObjectId(user_id)
    except Exception:
        return None
    return users.find_one({"_id": oid})


def find_users_by_city_pymongo(city: str) -> List[UserDict]:
    db = get_db()
    users = db["users"]
    return list(users.find({"profile.city": city}))


def update_user_email_pymongo(user_id: str, new_email: str) -> bool:
    db = get_db()
    users = db["users"]
    try:
        oid = ObjectId(user_id)
    except Exception:
        return False

    res = users.update_one({"_id": oid}, {"$set": {"email": new_email}})
    return res.modified_count == 1
