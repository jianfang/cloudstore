__author__ = 'jfang'

from flask import request, jsonify
from ..models import Post
from . import api

@api.route('/users/<int:id>/posts/', methods=['POST'])
def post(id):
    uid = id
    dict = request.args
    print(dict)
    title = dict['title']
    body = dict['body']
    new_post = Post.add_post(uid, title, body)
    if new_post is not None:
        return jsonify({'post_id': new_post.id, 'status': 'done'})

