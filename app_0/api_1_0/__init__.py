__author__ = 'sid'

from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, posts, comments, errors
from app_0.api_1_0 import users, errors, authentication, comments, posts
