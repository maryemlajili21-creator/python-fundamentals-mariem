from mongoengine import connect


def init_mongoengine() -> None:
    """Connect to MongoDB without Docker."""
    connect(
        db="users_db",
        host="localhost",
        port=27017,
        alias="default",
    )
