"""
https://docs.peewee-orm.com/en/latest/index.html
"""
from peewee import SqliteDatabase
from peewee import Model
from peewee import ForeignKeyField
from peewee import CharField
from peewee import DateTimeField
from peewee import TextField

DATABASE = 'test.db'

database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()


class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')

    class Meta:
        indexes = (
            (('from_user', 'to_user'), True),
        )


class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages')
    content = TextField()
    pub_date = DateTimeField()


def create_tables():
    with database:
        database.create_tables([User, Relationship, Message])


if __name__ == '__main__':
    create_tables()
    try:
        with database.atomic():
            user = User.create(
                username="andy",
                password="mypw",  # encrypt?
                email="andy@somewhere.com",
                join_date="01/01/2024")

    except Exception as e:
        print("ERROR")
