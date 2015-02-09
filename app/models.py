__author__ = 'sid'

from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mongoalchemy.document import Index
from flask.ext.mongoalchemy import MongoAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db


class Post(db.Document):
    pass


class User(db.Document):
    pass


class Idol(db.Document):
    # fields
    id = db.IntField()
    name = db.StringField()
    stage_name = db.StringField()
    birthday = db.DateTimeField()
    member_since = db.CreatedField()

    # optional fields
    posts = db.ListField(db.SRefField(Post), default_empty=True)
    followers = db.ListField(db.SRefField(User), default_empty=True)

    # index
    name_index = Index().descending('name').unique()


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
    posts = db.ListField(db.SRefField(Post), default_empty=True)

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

    @staticmethod
    def get_user(uid):
        user = User.query.filter(User.mongo_id==uid).first()
        return user

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'username': self.username}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.filter(User.username==data['username']).first()

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=str(self.mongo_id), _external=True),
            'username': self.username,
        }
        return json_user


class Post(db.Document):
    # fields
    id = db.IntField()
    title = db.StringField()
    body = db.StringField()
    timestamp = db.CreatedField()
    author_id = db.SRefField(User)

    @staticmethod
    def add_post(uid, title, body):
        user = User.query.filter(User.mongo_id==uid).first()
        post = Post(id=0, title=title, body=body, author_id=user.mongo_id)
        post.save()
        user.posts.append(post.mongo_id)
        user.save()
        return post

    @staticmethod
    def get_post(pid):
        return Post.query.filter(Post.mongo_id==pid).first()

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=str(self.mongo_id), _external=True),
            'title': self.title,
            'body': self.body,
            'create_at': self.timestamp,
            'author_url': url_for('api.get_user', id=str(self.author_id), _external=True)
        }
        return json_post
