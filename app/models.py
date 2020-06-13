from app import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Users(db.Model):
    roles = {
        1: 'ADMIN',
        2: 'USER'
    }
    __tablename__ = 'ak_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    name_cn = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(32))
    phone = db.Column(db.String(11))
    role = db.Column(db.String(16))
    is_active = db.Column(db.Boolean)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def getnerate_rest_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode("utf8")

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name_cn': self.name_cn,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active
        }