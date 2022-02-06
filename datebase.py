from peewee import *

db = SqliteDatabase('db.db')


class User(Model):
    message_chat_id = PrimaryKeyField(unique=True)
    name = CharField(null=True)
    city = CharField(null=True)
    phone = IntegerField(null=True)
    mail = IntegerField(null=True)
    platform_type = IntegerField(null=True)

    class Meta:
        database = db
        order_by = 'message_chat_id'
        db_table = 'users'
