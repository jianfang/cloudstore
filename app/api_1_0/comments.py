__author__ = 'sid'

from bson import ObjectId
from flask import jsonify, request
from . import api
from ..models import User, Post, Comment


@api.route('/posts/<id>/comment', methods=['POST'])
def new_post_comment(id):
    dict = request.values
    print(dict)
    body = dict['body']
    aid = dict['author']
    pid = ObjectId(str(id))
    post = Post.get_post(pid)
    if post is not None:
        uid = ObjectId(str(aid))
        user = User.get_user(uid)
        if user is not None:
            comment = Comment.add_comment(user, post, body)
    return jsonify({'status': 'done'})


@api.route('/comments/<id>', methods=['GET'])
def get_comment(id):
    cid = ObjectId(str(id))
    comment = Comment.get_comment(cid)
    if comment is not None:
        return jsonify(comment.to_json())


