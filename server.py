__author__ = 'sid'

from json import JSONEncoder
from datetime import datetime

from flask import Flask, request, jsonify
from flaskmimerender import mimerender
from qn import *

render_xml = lambda message: '<message>%s</message>' % message
render_json = jsonify
#render_html = lambda message: '<html><body>%s</body></html>' % message
render_html = jsonify
render_txt = lambda message: message

app = Flask(__name__)
counter = 0

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

@app.route("/download-url")
@mimerender(
        default = 'json',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
)
def download_url():
    if request.method == 'GET':
        private_key = request.args.get('file')
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
    gossip['text'] = 'blahblah...'
    gossip['idol'] = 'XXX'
    return gossip

@app.route("/api/gossips")
@mimerender(
        default = 'json',
        html = render_html,
        xml  = render_xml,
        json = render_json,
        txt  = render_txt
)
def gossips():
    if request.method == 'GET':
        gossip_list = []
        for i in range(0, 10):
            gossip_list.append(get_gossip())
        gossip = {}
        gossip['gossip'] = gossip_list
        gossips = {}
        gossips['gossips'] = gossip
        gossips['stat'] = 'ok'
        return gossips

if __name__ == "__main__":
    app.run(host='0.0.0.0')
