__author__ = 'sid'

from werkzeug.security import generate_password_hash, check_password_hash
from mongoalchemy.document import Index
from flask.ext.mongoalchemy import MongoAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db


class Post(db.Document):
    pass


class User(db.Document):
    # fields
    id = db.IntField()
    email = db.StringField(max_length=64)
    username = db.StringField()
    password_hash = db.StringField()
    member_since = db.CreatedField()
    confirmed = db.BoolField()

    # optional fields
    phone = db.StringField(required=False)
    posts = db.ListField(db.RefField(db.DocumentField(Post)), default_empty=True)

    # index
    email_index = Index().descending('email').unique()
    username_index = Index().descending('username').unique()

    @staticmethod
    def generate_fake(count=100):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(id=0,
                     email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password_hash=generate_password_hash(forgery_py.lorem_ipsum.word()),
                     confirmed=False
                     # password=forgery_py.lorem_ipsum.word()
                     # location=forgery_py.address.city(),
                     # about_me=forgery_py.lorem_ipsum.sentence(),
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
        user = User(id=id, email=email, username=username,
                    password_hash=generate_password_hash(password),
                    confirmed=False)
        user.save()
        return user

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


class Post(db.Document):
    # fields
    id = db.IntField()
    title = db.StringField()
    body = db.StringField()
    timestamp = db.CreatedField()
    author = db.RefField(User)

    @staticmethod
    def add_post(uid, title, body):
        id = 0
        post = Post(id=id, title=title, body=body, author=None)
        post.save()
        return post

