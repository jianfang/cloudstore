__author__ = 'sid'

from datetime import datetime
from bson import ObjectId
from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from mongoalchemy.document import Index
from flask.ext.mongoalchemy import BaseQuery
from flask.ext.mongoalchemy import MongoAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db


class Post(db.Document):
    pass

class User(db.Document):
    pass

class Comment(db.Document):
    pass


class Idol(db.Document):
    # fields
    id = db.IntField()
    name = db.StringField()
    stage_name = db.StringField()
    birthday = db.DateTimeField()
    time_added = db.CreatedField()
    avatar = db.StringField()
    last_posted = db.DateTimeField()

    # optional fields
    posts = db.ListField(db.SRefField(Post), default_empty=True)
    followers = db.ListField(db.SRefField(User), default_empty=True)

    # index
    name_index = Index().descending('name').unique()

    @staticmethod
    def add_idol(name, stage_name, birthday, avatar):
        id = 0
        date_object = datetime.strptime(birthday, '%Y/%m/%d')
        idol = Idol(id=id, name=name, stage_name=stage_name,
                    birthday=date_object, avatar=avatar)
        idol.save()
        return idol

    @staticmethod
    def validate_idol(name):
        if Idol.query.filter_by(name=name).first():
            raise ValidationError('Idol already exists.', 'IDOL_ALREADY_EXISTS')

    @staticmethod
    def get_idol(id):
        iid = ObjectId(str(id))
        idol = Idol.query.filter(Idol.mongo_id == iid).first()
        return idol

    def add_post(self, post):
        self.posts.append(post.mongo_id)
        self.last_posted = datetime.utcnow()
        self.save()

    def to_json(self):
        json_idol = {
            'id': str(self.mongo_id),
            'url': url_for('api.get_idol', id=str(self.mongo_id), _external=True),
            'name': self.name,
            'stage_name': self.stage_name,
            'follower_count': len(self.followers),
            'avatar': self.avatar
        }
        return json_idol


class User(db.Document):
    # fields
    id = db.IntField()
    email = db.StringField(max_length=64)
    username = db.StringField()
    password_hash = db.StringField()
    member_since = db.CreatedField()
    confirmed = db.BoolField()

    # optional fields
    avatar = db.StringField(required=False)
    phone = db.StringField(required=False)
    followed = db.ListField(db.SRefField(Idol), default_empty=True)
    posts = db.ListField(db.SRefField(Post), default_empty=True)
    comments = db.ListField(db.SRefField(Comment), default_empty=True)

    # index
    #email_index = Index().descending('email').unique()
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
            raise ValidationError('Username already in use.', 'USER_ALREADY_EXISTS')

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
        user = User.query.filter(User.mongo_id == uid).first()
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
            'id': str(self.mongo_id),
            'url': url_for('api.get_user', id=str(self.mongo_id), _external=True),
            'username': self.username,
            'avatar': self.avatar,
            'followed': [str(f) for f in self.followed]
        }
        return json_user

    def to_json_simple(self):
        json_user = {
            'id': str(self.mongo_id),
            'name': self.username,
            'avatar': self.avatar,
        }
        return json_user

class MyCustomizedQuery(BaseQuery):

    def get_posts_for_idol(self, idol):
        return self.filter(self.type.idol == ObjectId(idol))


class Post(db.Document):
    query_class = MyCustomizedQuery

    # fields
    id = db.IntField()
    title = db.StringField()
    text = db.StringField()
    photo = db.StringField()
    timestamp = db.CreatedField()
    author = db.SRefField(User)
    idol = db.SRefField(Idol)
    comments = db.ListField(db.SRefField(Comment), default_empty=True)

    # static members
    LAST_POSTED = datetime.utcnow()

    @staticmethod
    def to_json_no_update():
        json_no_update = {
            'posts': {
                        'count': 0
             },
            'stat': 'ok'
        }
        return json_no_update

    @staticmethod
    def add_post(user, idol, body, photo):
        post = Post(id=0, title='', text=body, author=user.mongo_id, idol=idol.mongo_id, photo=photo)
        post.save()
        user.posts.append(post.mongo_id)
        user.save()
        idol.add_post(post)
        Post.LAST_POSTED = datetime.utcnow()
        return post

    @staticmethod
    def get_post(pid):
        return Post.query.filter(Post.mongo_id==pid).first()

    def to_json(self):
        author = User.get_user(self.author)

        json_post = {
            'id': str(self.mongo_id),
            'url': url_for('api.get_post', id=str(self.mongo_id), _external=True),
            'idol': str(self.idol),
            'title': self.title,
            'text': self.text,
            'photo': self.photo,
            'create_at': str(self.timestamp),
            'author': author.to_json_simple(),
            'comments': {
                'count': len(self.comments),
                'comment': [
                ]
            }
        }
        return json_post


class Comment(db.Document):
    #fields
    id = db.IntField()
    body = db.StringField()
    timestamp = db.CreatedField()
    author = db.SRefField(User)
    post = db.SRefField(Post)

    @staticmethod
    def add_comment(user, post, body):
        comment = Comment(id=0, body=body, post=post.mongo_id, author=user.mongo_id)
        comment.save()
        user.comments.append(comment.mongo_id)
        user.save()
        post.comments.append(comment.mongo_id)
        post.save()
        return comment

    @staticmethod
    def get_comment(cid):
        return Comment.query.filter(Comment.mongo_id==cid).first()

    def to_json(self):
        author = User.get_user(self.author)
        json_comment = {
            'id': str(self.mongo_id),
            'body': self.body,
            'create_at': str(self.timestamp),
            'author': author.to_json_simple(),
            'post': str(self.post)
        }
        return json_comment
