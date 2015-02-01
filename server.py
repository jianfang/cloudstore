__author__ = 'sid'

from datetime import datetime

from flask import Flask, request, jsonify, abort
from flaskmimerender import mimerender

from qn import *

render_xml = lambda message: '<message>%s</message>' % message
render_json = jsonify
#render_html = lambda message: '<html><body>%s</body></html>' % message
render_html = jsonify
render_txt = lambda message: message

app = Flask(__name__)
counter = 0

users = [
    {
        'name': 'First User',
        'unique': 0
    }
]

idols = [
    {
        'name': 'No.1',
        'stageName': 'No.1',
        'iconUrl': '',
        'unique': 0
    }
]

gossips = [
    {
        'title': 'DUMMY',
        'text': 'blahblah...,blahblah...blahblah...,blahblah...,blahblah...,blahblah...,blahblah...,blahblah...',
        'time': str(datetime.now()),
        'image': '',
        'idol_id': 0,
        'author_id': 0,
        'unique': '0'
    }
]

gossip_comments = [
    {
        'text': 'words in comment',
        'gossip_id': 0,
        'author_id': 0,
        'time': str(datetime.now()),
        'unique': '0'
    }
]

@app.route("/")
@mimerender(
        default = 'html',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
)
def hello():
    if request.method == 'GET':
        global counter
        counter += 1
        return {'id':counter,'content':'Hello World!'}

@app.route("/upload-token")
@mimerender(
        default = 'json',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
)
def upload_token():
    if request.method == 'GET':
        key = get_unique_filename()
        token = get_upload_token(key)
        return {'key':key, 'token':token}

@app.route("/download-url/<file>")
@mimerender(
        default = 'json',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
)
def download_url(file):
    if request.method == 'GET':
        private_key = file
        url = get_download_url(private_key)
        return {'key':private_key, 'url':url}

def get_gossip():
    gossip = {}
    global counter
    gossip['id'] = str(counter)
    counter += 1
    gossip['datetime'] = str(datetime.now())
    gossip['title'] = 'DUMMY'
    gossip['author'] = 'g1'
    gossip['text'] = 'blahblah...,blahblah...blahblah...,blahblah...,blahblah...,blahblah...,blahblah...,blahblah...'
    gossip['idol'] = 'XXX'
    return gossip

@app.route("/api/gossips", methods=['GET'])
def get_gossips():
    # gossip_list = []
    # for i in range(0, 10):
    #     gossip_list.append(get_gossip())
    g = {}
    g['gossip'] = gossips
    gs = {}
    gs['gossips'] = g
    gs['stat'] = 'ok'
    return jsonify(gs)

@app.route("/api/gossips/<int:id>/comments", methods=['GET'])
def get_comments(id):
    if id == '':
        abort(400)
    comment = [comment for comment in gossip_comments if comment['gossip_id'] == id]
    if len(comment) == 0:
        abort(404)
    return jsonify({'comment': comment})

@app.route("/api/gossips", methods=['POST'])
def add_gossip():
    if not request.json or not 'title' in request.json:
        abort(400)
    gossip = {
        'title': request.json['title'],
        'text': request.json.get('text', 'blahblah...,blahblah...blahblah...,blahblah...,blahblah...,blahblah...,blahblah...,blahblah...'),
        'time': str(datetime.now()),
        'image': request.json.get('image', ''),
        'idol_id': request.json.get('idol_id', ''),
        'author_id': request.json.get('author_id', ''),
        'unique': str(int(gossips[-1]['unique']) + 1)
    }
    gossips.append(gossip)
    return jsonify({'gossip': gossip}), 201

@app.route('/api/idols', methods=['POST'])
def add_idol():
    if not request.json or not 'name' in request.json:
        abort(400)
    idol = {
        'name': request.json['name'],
        'stageName': request.json.get('stageName', request.json['name']),
        'iconUrl': request.json.get('iconUrl', ""),
        'unique': idols[-1]['unique'] + 1
    }
    idols.append(idol)
    return jsonify({'idol': idol}), 201

if __name__ == "__main__":
    from app_0.api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    app.run(host='0.0.0.0')
