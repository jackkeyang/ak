from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app.models import Users
from app.errors import not_found
from app import db
from app.utils import login_role_required, self_required

mod = Blueprint('users', __name__)

# 登录
class LoginView(MethodView):
    def post(self):
        data = request.get_json()
        user = Users.query.filter_by(username = data.get('username')).first()
        if user  and user.is_active:
            if user.verify_password(data.get("password")):
                token = user.getnerate_rest_token()
                return jsonify({'code': 200, 'token': token})
            else:
                return jsonify({'code': 100, 'message': "密码错误"})
        else:
            return jsonify({'code': 100, 'message':'用户不存在或被锁定'})
mod.add_url_rule('login', view_func=LoginView.as_view("login"))

# 用户列表
class UserListView(MethodView):
    decorators = [login_role_required('USER')]
    def get(self):
        userlist = Users.query.all()
        return jsonify([ u.to_json() for u in userlist])
mod.add_url_rule('userlist', view_func=UserListView.as_view("userlist"))

# 用户信息查看和修改
class UserInfoView(MethodView):
    decorators = [login_role_required('USER'), self_required]
    def get(self):
        username = request.get_json().get('username', None)
        user = Users.query.filter_by(username = username).first()
        if user:
            return jsonify(user.to_json())
        else:
            return not_found()
    def post(self):
        data = request.get_json()
        username = data.get('username',None)
        if data.get('role'):
            data['role'] = Users.roles.get(int(data.get('role')))
        if Users.query.filter_by(username = username).update(data):
            db.session.commit()
            return jsonify({'code': 200, 'message': '用户更新成功'})
        else:
            return jsonify({'code': 100, 'message': '用户更新失败'})
mod.add_url_rule('userinfo', view_func=UserInfoView.as_view("userinfo"))

# 修改密码
class ModyfiPasswdView(MethodView):
    decorators = [login_role_required('USER'), self_required]
    def post(self):
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        user = Users.query.filter_by(username=username).first()
        if user:
            user.password = password
            db.session.commit()
            return jsonify({"code": 200, "message": "密码修改成功"})
        else:
            return jsonify({"code": 100, "message": "用户不存在"})
mod.add_url_rule('modifypasswd', view_func=ModyfiPasswdView.as_view("modifypasswd"))

# 删除用户
class DeleteUserView(MethodView):
    decorators = [login_role_required('ADMIN')]
    def post(self):
        username = request.get_json().get('username')
        if username == "admin":
            return jsonify({'code': 100, 'message': '无法删除超级管理员'})
        user = Users.query.filter_by(username = username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'code':200, 'message': '用户删除成功'})
        else:
            return jsonify({"code": 100, "message": "用户不存在"})
mod.add_url_rule('deleteuser', view_func=DeleteUserView.as_view("deleteuser"))

# 添加用户
class AddUserView(MethodView):
    decorators = [login_role_required('ADMIN')]
    def post(self):
        data = request.get_json()
        username = Users.query.filter_by(username=data.get("username")).first()
        if username:
            return jsonify({'code': 100, 'message':'用户已存在'})
        print(data.get('phone'))
        user = Users(**data)
        user.password = "123456"
        db.session.add(user)
        db.session.commit()
        return jsonify({'code': 200, 'message': '用户添加成功'})
mod.add_url_rule('adduser', view_func=AddUserView.as_view("adduser"))