from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField


class DBPerson(Document):
    name = StringField()
    phones = ListField()
    birthday = DateTimeField()
    email = StringField()
    address = StringField()


class DBNote(Document):
    title = StringField()
    text = StringField()
    created = DateTimeField()
    tags = ListField()
