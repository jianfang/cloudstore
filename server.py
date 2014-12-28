__author__ = 'sid'

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

if __name__ == "__main__":
    app.run(host='0.0.0.0')
