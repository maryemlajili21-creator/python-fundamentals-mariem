from typing import Optional, List
from bson import ObjectId

from models_mongoengine import User, Profile


def create_user_me(username: str, email: str, age: int, city: str) -> str:
    profile = Profile(age=age, city=city)
    user = User(username=username, email=email, profile=profile)
    user.save()
    return str(user.id)


def get_user_by_id_me(user_id: str) -> Optional[User]:
    try:
        oid = ObjectId(user_id)
    except Exception:
        return None

    return User.objects(id=oid).first()


def find_users_by_city_me(city: str) -> List[User]:
    return list(User.objects(profile__city=city))


def update_user_email_me(user_id: str, new_email: str) -> bool:
    try:
        oid = ObjectId(user_id)
    except Exception:
        return False

    res = User.objects(id=oid).update_one(set__email=new_email)
    return res == 1
