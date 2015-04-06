__author__ = 'sid'

from bson import ObjectId
from flask import request, jsonify
from . import api
from ..models import Idol, Post

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
    idol = Idol.get_idol(id)
    if idol is not None:
        idols.append(idol.to_json())
    g['idol'] = idols
    gs['idols'] = g
    gs['stat'] = 'ok'
    return jsonify(gs)


@api.route('/idols/<id>/posts/', methods=['GET'])
def get_idol_posts(id):
    page = request.args.get('page', 1, type=int)
    gs = {}
    g = {}
    posts = []
    idol = Idol.get_idol(id)
    if idol is not None:
        for p in idol.posts:
            pid = ObjectId(str(p))
            post = Post.get_post(pid)
            posts.append(post.to_json())
    g['post'] = posts
    gs['posts'] = g
    gs['stat'] = 'ok'
    return jsonify(gs)
