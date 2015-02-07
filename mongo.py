__author__ = 'sid'

import os

from flask import Flask, jsonify, request
from flask.ext.mongoalchemy import MongoAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, create_app
from app.models import User
from app.api_1_0 import api


if __name__ == "__main__":
    app = create_app(os.getenv('FLASK_CONFIG') or 'development')

    # create a development user
    user = User.query.filter(User.username=='dev').first()
    if user is None:
        User.add_user('dev@app.com', 'dev', 'dev_password')

    app.run(host='0.0.0.0', debug=True)


