__author__ = 'sid'

from bson import ObjectId
from flask import request, jsonify
from . import api
from ..models import User, Idol
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
        return jsonify(user.to_json())

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
            user.followed.add(idol)
            user.save()
            idol.followers.add(user)
            idol.save()
        return jsonify(user.to_json())

