__author__ = 'sid'

from bson import ObjectId
from flask import request, jsonify
from . import api
from ..models import Idol

@api.route('/idols/', methods=['POST'])
def add_idol():
    dict = request.values
    print(dict)
    name = dict['name']
    Idol.validate_idol(name)
    stage_name = dict['stage_name']
    birthday = dict['birthday']
    avatar = dict['avatar']
    idol = Idol.add_idol(name, stage_name, birthday, avatar)
    if idol is not None:
        return jsonify({'name': idol.name, 'status': 'done'})


@api.route('/idols/', methods=['GET'])
def get_idols():
    gs = {}
    g = {}
    idols = []
    for idol in Idol.query.filter():
        if idol is not None:
            idols.append(idol.to_json())
    g['idol'] = idols
    gs['idols'] = g
    gs['stat'] = 'ok'
    return jsonify(gs)


@api.route('/idols/<id>', methods=['GET'])
def get_idol(id):
    gs = {}
    g = {}
    idols = []
    iid = ObjectId(str(id))
    idol = Idol.get_idol(iid)
    if idol is not None:
        idols.append(idol.to_json())
    g['idol'] = idols
    gs['idols'] = g
    gs['stat'] = 'ok'
    return jsonify(gs)


