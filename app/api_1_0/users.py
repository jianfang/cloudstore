__author__ = 'sid'

from bson import ObjectId
from flask import request, jsonify
from . import api
from ..models import User
from ..exceptions import ValidationError

@api.route('/')
def main():
    return jsonify({'message':'hello'})

@api.route('/register', methods=['POST'])
def register():
    dict = request.args
    print(dict)
    email = dict['email']
    User.validate_email(email)
    username = dict['username']
    User.validate_username(username)
    password = dict['password']
    user = User.add_user(email, username, password)
    if user is not None:
        return jsonify({'user_id': user.id, 'status': 'done'})


@api.route('/users/<id>', methods=['GET'])
def get_user(id):
    uid = ObjectId(str(id))
    user = User.get_user(uid)
    if user is not None:
        return jsonify(user.to_json())

