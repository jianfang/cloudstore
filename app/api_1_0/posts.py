__author__ = 'jfang'


from datetime import datetime, timedelta, tzinfo
from bson import ObjectId
from mongoalchemy.query_expression import QueryField
from flask import request, jsonify, current_app
from ..models import Idol, Post, Comment
from . import api

class ShanghaiTimeZone(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=8)
    def dst(self, dt):
        return timedelta(hours=0)

class utcTimeZone(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=0)
    def dst(self, dt):
        return timedelta(hours=0)

def is_updated(time, refresh_time):
    if refresh_time == '':
        return False
    refresh = datetime.strptime(refresh_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=ShanghaiTimeZone())
    time = time.replace(tzinfo=utcTimeZone())
    return time < refresh


@api.route('/posts/', methods=['GET'])
def get_posts():
    last_refresh = request.args.get('last_refresh', '', type=str)
    page = request.args.get('page', 1, type=int)
    idol_id = request.args.get('idol', '', type=str)
    time_field = QueryField(Post.timestamp)
    if idol_id == '':
        pagination = Post.query.descending(time_field).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
        posts = pagination.items
    else:
        idol = Idol.get_idol(idol_id)
        if idol:
            if is_updated(idol.last_posted, last_refresh):
                return jsonify({
                   'posts': {
                        'count': 0
                    },
                    'stat': 'ok'
                })

        pagination = Post.query.get_posts_for_idol(idol_id).descending(time_field).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
        posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = page-1
    next = None
    if pagination.has_next:
        next = page+1
    return jsonify({
        'posts': {
            'post': [post.to_json() for post in posts],
            'prev': prev,
            'next': next,
            'count': pagination.total,
            'pages': pagination.pages
        },
        'stat': 'ok'
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


