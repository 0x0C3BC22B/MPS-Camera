from django.db import models
import datetime
from mongoengine import Document, StringField, IntField, DateTimeField,EmbeddedDocument,ListField,EmbeddedDocumentField

class Vendors(EmbeddedDocument):
    """
    Vendors model for storing vendor information.
    """
    name = StringField(required=True, max_length=100)
    contact = StringField(max_length=100)
    address = StringField(max_length=200)

class CameraModel(EmbeddedDocument):
    """
    CameraModel model for storing camera model information.
    """
    name = StringField(required=True, max_length=100)
    vendor = ListField(EmbeddedDocumentField(Vendors))

class IPCamera(Document):
    """
    IPCamera model for storing camera information.
    """
    name = StringField(required=True, max_length=100)
    ip_address = StringField(required=True, max_length=15)
    port = IntField(default=80)
    model = ListField(EmbeddedDocumentField(CameraModel)),
    created_at = DateTimeField()
    updated_at = DateTimeField()
    status = StringField(default="inactive")
    mac = StringField(max_length=17)
    username = StringField(max_length=50)
    password = StringField(max_length=100)
    serial_number = StringField(max_length=50)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(IPCamera, self).save(*args, **kwargs)
