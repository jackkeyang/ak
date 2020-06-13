from flask import Flask, jsonify
from config import *
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)


def create_app(app_name):
    app.config.from_object(config[app_name])

    db.init_app(app)

    from app.views import users
    app.register_blueprint(users.mod, url_prefix='/api')

    from app.views import hosts
    app.register_blueprint(hosts.mod, url_prefix='/api')

    return app