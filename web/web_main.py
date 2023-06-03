from flask import Flask
from .plugins import app_plugins

app = Flask(__name__)
app.register_blueprint(app_plugins)

def main():
    app.run(host='127.0.0.1', port=6000)
