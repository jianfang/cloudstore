__author__ = 'sid'

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.mongoalchemy import MongoAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db

class User(db.Document):
    id = db.IntField()
    email = db.StringField()
    username = db.StringField()
    password_hash = db.StringField()

    @staticmethod
    def generate_fake(count=100):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password_hash=generate_password_hash(forgery_py.lorem_ipsum.word()),
                     id=0
                     # password=forgery_py.lorem_ipsum.word()
                     # confirmed=True,
                     # name=forgery_py.name.full_name(),
                     # location=forgery_py.address.city(),
                     # about_me=forgery_py.lorem_ipsum.sentence(),
                     # member_since=forgery_py.date.date(True)
            )
            u.save()

    @staticmethod
    def validate_email(email):
        if User.query.filter_by(email=email).first():
            raise ValidationError('Email already registered.')

    @staticmethod
    def validate_username(username):
        if User.query.filter_by(username=username).first():
            raise ValidationError('Username already in use.')

    @staticmethod
    def add_user(email, username, password):
        id = 0
        user = User(email=email, username=username,
                    password_hash=generate_password_hash(password), id=id)
        user.save()
        return user

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

