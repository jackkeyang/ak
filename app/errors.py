from app import app
from flask import jsonify


@app.errorhandler(401)
def auth_error():
    return jsonify({"code": 401, "message": "验证失败"})

@app.errorhandler(403)
def request_error():
    return jsonify({"code": 403, "message": "请求错误"})

@app.errorhandler(404)
def not_found():
    return jsonify({"code": 404, "message": "Not Found"})

