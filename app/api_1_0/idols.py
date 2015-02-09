__author__ = 'sid'

from bson import ObjectId
from flask import request, jsonify
from . import api
from ..models import Idol

@api.route('/idols/', methods=['POST'])
def add_idol():
    dict = request.args
    print(dict)
    name = dict['name']
    stage_name = dict['stage_name']
    birthday = dict['birthday']
    idol = Idol.add_idol(name, stage_name, birthday)
    if idol is not None:
        return jsonify({'name': idol.name, 'status': 'done'})


@api.route('/idols/<id>', methods=['GET'])
def get_idol(id):
    iid = ObjectId(str(id))
    idol = Idol.get_idol(iid)
    if idol is not None:
        return jsonify(idol.to_json())



