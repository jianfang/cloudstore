__author__ = 'sid'

import os

from flask import Flask, jsonify, request
from flask.ext.mongoalchemy import MongoAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, create_app
from app.models import User
from app.api_1_0 import api

app = Flask(__name__)
#app.config['MONGOALCHEMY_DATABASE'] = 'user'


if __name__ == "__main__":
    #db.init_app(app)
    #with app_0.app_context():
    #    db.ensure_index({'username': 1}, unique=True)
    #from app.models import User
    #User.generate_fake()

    app = create_app(os.getenv('FLASK_CONFIG') or 'development')
    app.run(host='0.0.0.0', debug=True)


