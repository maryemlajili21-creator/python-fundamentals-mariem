from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
    EmailField,
    IntField,
)


class Profile(EmbeddedDocument):
    age = IntField(required=True)
    city = StringField(required=True)


class User(Document):
    meta = {"collection": "users"}
    username = StringField(required=True, unique=True)
    email = EmailField(required=True)
    profile = EmbeddedDocumentField(Profile, required=True)
