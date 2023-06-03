from flask import send_file, make_response
from . import app_plugins

app = app_plugins

@app.route('/')
def index():
    url = "templates/index/"
    html = url + "index.html"
    return send_file(html)

@app.route('/index_old')
def index_old():
    url = "templates/index_old/"
    html = url + "index.html"
    return send_file(html)
