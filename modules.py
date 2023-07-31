from tortoise.models import Model
from tortoise import fields


class Hotel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    description = fields.TextField(null=False)
    stars = fields.IntField(null=False)
    minimal_price = fields.IntField(null=False)


class Room(Model):
    id = fields.IntField(pk=True)
    hotel = fields.ForeignKeyField("modules.Hotel", related_name="rooms")
    count_of_person = fields.IntField(null=False)
    price = fields.IntField(null=False)


class Client(Model):
    id = fields.IntField(pk=True)
    room = fields.ForeignKeyField("modules.Room", related_name="clients")
    full_name = fields.CharField(max_length=255, null=False)
    phone_number = fields.CharField(max_length=50, null=False)
    date_start = fields.CharField(max_length=30, null=False)
    date_end = fields.CharField(max_length=30, null=False)
