from functools import wraps
from flask import request, current_app
from app.models import Users
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.errors import auth_error, request_error

def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    data = s.loads(token)
    return Users.query.get(data['id'])

# 验证token，并且判断role
def login_role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                token = request.headers.get("token")
                user = verify_auth_token(token)
                if role == 'ADMIN':
                    return func(*args, **kwargs)
                if user.role != role:
                    return auth_error()
                return func(*args, **kwargs)
            except Exception as e:
                print(e)
                return auth_error()
        return wrapper
    return decorator

# 判断请求是否是自己, 管理员无限制
def self_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            username = request.get_json().get("username")
            token = request.headers.get("token")
            user = verify_auth_token(token)
            if user.role == 'ADMIN':
                return func(*args, **kwargs)
            if user.username != username:
                return request_error()
        except:
            return request_error()
        return func(*args, **kwargs)
    return wrapper
