# 资源（css、js、img）
from flask import request, send_file
from . import app_plugins
from urllib.parse import urlparse

app = app_plugins

@app.route('/<folder>/<path:path>')
def resources(folder,path):
    if folder in ['css', 'js', 'img']:
        referer_url = request.headers.get('Referer')
        parsed_url = urlparse(referer_url)
        hostname = parsed_url.hostname
        path_parts = parsed_url.path.split("/")
        directory = path_parts[1]
        if directory == "":
            directory = "index"
        url = f"templates/{directory}/{folder}/{path}"
        return send_file(url)