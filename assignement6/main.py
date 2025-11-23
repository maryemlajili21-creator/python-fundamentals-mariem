from pprint import pprint

from crud_pymongo import (
    create_user_pymongo,
    get_user_by_id_pymongo,
    find_users_by_city_pymongo,
    update_user_email_pymongo,
)

from db_mongoengine import init_mongoengine
from crud_mongoengine import (
    create_user_me,
    get_user_by_id_me,
    find_users_by_city_me,
    update_user_email_me,
)


def test_pymongo():
    print("\nPyMongo")
    uid = create_user_pymongo("lina", "lina@ex.com", 25, "paris")
    print("Created:", uid)


    pprint(find_users_by_city_pymongo("paris"))

    print("Update email:")
    pprint(update_user_email_pymongo(uid, "lina_new@ex.com"))


def test_mongoengine():
    print("\nMongoEngine ")
    init_mongoengine()

    uid = create_user_me("ajmi", "ajmi@ex.com", 25, "tunis")
    print("Created:", uid)

  


    for u in find_users_by_city_me("tunis"):
        print(u.to_mongo())

    print("Update email:")
    pprint(update_user_email_me(uid, "ajmi_new@ex.com"))


if __name__ == "__main__":
    test_pymongo()
    test_mongoengine()
