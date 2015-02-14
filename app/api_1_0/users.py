__author__ = 'sid'

from bson import ObjectId
from flask import request, jsonify
from . import api
from ..models import User
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

@api.route('/login', methods=['POST'])
def login():
    dict = request.args
    print(dict)
    email = dict['email']
    password = dict['password']
    user = User.query.filter_by(email=email).first()
    #    if user is not None and user.verify_password(password):
    #user = User.add_user(email, username, password)
    #if user is not None:
    #    return jsonify({'user_id': user.id, 'status': 'done'})

