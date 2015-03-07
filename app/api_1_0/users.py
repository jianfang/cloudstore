__author__ = 'sid'

from bson import ObjectId
from flask import request, jsonify
from . import api
from ..models import User, Idol, Post
from ..exceptions import ValidationError


@api.route('/')
def main():
    return jsonify({'message':'hello'})

@api.route('/users/', methods=['GET'])
def get_users():
    users = []
    for user in User.query.filter():
        if user is not None:
            users.append(user.to_json())
    return jsonify({'users': users})


@api.route('/users/<id>', methods=['GET'])
def get_user(id):
    uid = ObjectId(str(id))
    user = User.get_user(uid)
    if user is not None:
        return jsonify({'user': user.to_json(),
                        'status': 'done'})
    return jsonify({'status': 'failed'})


@api.route('/users/<id>/follow', methods=['POST'])
def follow(id):
    dict = request.values
    idol_id = dict['idol']
    iid = ObjectId(idol_id)
    idol = Idol.get_idol(iid)
    if idol is not None:
        uid = ObjectId(str(id))
        user = User.get_user(uid)
        if user is not None:
            if not (idol.mongo_id in user.followed):
                user.followed.append(idol.mongo_id)
                user.save()
            if not (user.mongo_id in idol.followers):
                idol.followers.append(user.mongo_id)
                idol.save()
            return jsonify({'status': 'done'})

    return jsonify({'status': 'failed'})


@api.route('/users/<id>/unfollow', methods=['POST'])
def unfollow(id):
    dict = request.values
    idol_id = dict['idol']
    iid = ObjectId(idol_id)
    idol = Idol.get_idol(iid)
    if idol is not None:
        uid = ObjectId(str(id))
        user = User.get_user(uid)
        if user is not None:
            if idol.mongo_id in user.followed:
                user.followed.remove(idol.mongo_id)
                user.save()
            if user.mongo_id in idol.followers:
                idol.followers.remove(user.mongo_id)
                idol.save()
            return jsonify({'status': 'done'})

    return jsonify({'status': 'failed'})


@api.route('/users/<id>/post', methods=['POST'])
def add_post(id):
    dict = request.values
    idol_id = dict['idol']
    iid = ObjectId(idol_id)
    idol = Idol.get_idol(iid)
    if idol is not None:
        uid = ObjectId(str(id))
        user = User.get_user(uid)
        if user is not None:
            body = dict['body']
            photo = dict['photo']
            new_post = Post.add_post(user, idol, body, photo)
            return jsonify({'post_id': str(new_post.mongo_id), 'status': 'done'})

    return jsonify({'status': 'failed'})

