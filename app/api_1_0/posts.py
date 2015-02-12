__author__ = 'jfang'

from bson import ObjectId
from flask import request, jsonify
from ..models import Post
from . import api

@api.route('/users/<id>/posts/', methods=['POST'])
def add_post(id):
    uid = ObjectId(str(id))
    dict = request.args
    #print(dict)
    title = dict['title']
    body = dict['body']
    new_post = Post.add_post(uid, title, body)
    if new_post is not None:
        return jsonify({'post_id': str(new_post.mongo_id), 'status': 'done'})

@api.route('/posts/', methods=['GET'])
def get_posts():
    posts = []
    for post in Post.query.filter():
        if post is not None:
            posts.append(post.to_json())
    return jsonify({'posts': posts})

@api.route('/posts/<id>', methods=['GET'])
def get_post(id):
    pid = ObjectId(str(id))
    post = Post.get_post(pid)
    if post is not None:
        return jsonify(post.to_json())




