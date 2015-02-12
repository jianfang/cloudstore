__author__ = 'sid'

import os
from flask import Flask, request, jsonify, g
from flask.ext.mongoalchemy import MongoAlchemy
from .exceptions import ValidationError
from .decorators import json, no_cache, rate_limit

db = MongoAlchemy()

def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)

    # apply configuration
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    # initialize extensions
    db.init_app(app)

    # register blueprints
    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # register an after request handler
    @app.after_request
    def after_request(rv):
        headers = getattr(g, 'headers', {})
        rv.headers.extend(headers)
        return rv

    @app.errorhandler(ValidationError)
    def validation_error(e):
        return bad_request(e.args[0])

    # register route
    from .models import User
    @app.route('/register', methods=['POST'])
    @rate_limit(10, 60)  # one call per 1 minute period
    @no_cache
    @json
    def register():
        dict = request.args
        print(dict)
        #email = dict['email']
        #User.validate_email(email)
        username = dict['username']
        User.validate_username(username)
        password = dict['password']
        user = User.add_user('', username, password)
        if user is not None:
            return {'user_id': user.id, 'status': 'done'}

    # authentication token route
    from .auth import auth
    @app.route('/get-auth-token')
    @auth.login_required
    @rate_limit(1, 60)  # one call per 1 minute period
    @no_cache
    @json
    def get_auth_token():
        import time
        time.sleep(5)
        return {'token': g.user.generate_auth_token(), 'status': 'done'}

    return app
