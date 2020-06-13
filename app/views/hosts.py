from flask import Blueprint, jsonify
from flask.views import MethodView

mod = Blueprint('hosts', __name__)

class HostView(MethodView):
    def get(self):
        return "host get"
    def post(self):
        return "host post"
mod.add_url_rule('hostlist', view_func=HostView.as_view("hostlist"))

