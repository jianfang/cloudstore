__author__ = 'sid'

from flask import jsonify
from . import api

@api.route('/gossips/<int:id>/comments/', methods=['POST'])
#@permission_required(Permission.COMMENT)
def new_post_comment(id):
    print(id)
    return jsonify({'gossip_id':id})
    # post = Post.query.get_or_404(id)
    # comment = Comment.from_json(request.json)
    # comment.author = g.current_user
    # comment.post = post
    # db.session.add(comment)
    # db.session.commit()
    # return jsonify(comment.to_json()), 201, \
    #     {'Location': url_for('api.get_comment', id=comment.id,
    #                          _external=True)}
