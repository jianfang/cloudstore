__author__ = 'sid'

from flask import request, jsonify
from . import api
from ..models import Idol

@api.route('/idols', methods=['POST'])
def add_idol():
    dict = request.args
    print(dict)
    email = dict['email']
    Idol.validate_email(email)
    username = dict['username']
    Idol.validate_username(username)
    user = Idol.add_idol(email, username)
    if user is not None:
        return jsonify({'user_id': user.id, 'status': 'done'})

