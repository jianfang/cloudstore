__author__ = 'jfang'

from bson import ObjectId
from flask import request, jsonify, current_app
from ..models import Post
from . import api

# @api.route('/users/<id>/posts/', methods=['POST'])
# def add_post(id):
#     uid = ObjectId(str(id))
#     dict = request.args
#     #print(dict)
#     title = dict['title']
#     body = dict['body']
#     new_post = Post.add_post(uid, title, body)
#     if new_post is not None:
#         return jsonify({'post_id': str(new_post.mongo_id), 'status': 'done'})

@api.route('/posts/', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = page-1
    next = None
    if pagination.has_next:
        next = page+1
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total,
        'pages': pagination.pages
    })


@api.route('/posts/<id>', methods=['GET'])
def get_post(id):
    pid = ObjectId(str(id))
    post = Post.get_post(pid)
    if post is not None:
        return jsonify(post.to_json())




