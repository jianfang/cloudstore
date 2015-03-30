__author__ = 'jfang'

from bson import ObjectId
from mongoalchemy.query_expression import QueryField
from flask import request, jsonify, current_app
from ..models import Post, Comment
from . import api


@api.route('/posts/', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    idol = request.args.get('idol', '', type=str)
    time_field = QueryField(Post.timestamp)
    if idol == '':
        pagination = Post.query.descending(time_field).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
        posts = pagination.items
    else:
        pagination = Post.query.get_posts_for_idol(idol).descending(time_field).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
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


@api.route('/posts/<id>/comments/', methods=['GET'])
def get_post_comments(id):
    gs = {}
    g = {}
    pid = ObjectId(str(id))
    post = Post.get_post(pid)
    comments = []
    if post is not None:
        for c in post.comments:
            cid = ObjectId(str(c))
            comment = Comment.get_comment(cid)
            comments.append(comment.to_json())
    g['comment'] = comments
    gs['comments'] = g
    gs['stat'] = 'ok'
    return jsonify(gs)


