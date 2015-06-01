#-*- coding: UTF-8 -*-

from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from .permission import Permission

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class AnonymousUser(AnonymousUserMixin):

    def can(self, permissons):
        return False

    def is_administrator(self):
        return False

class User(UserMixin, db.Model):

    '''用户表，字段包括：
    用户ID，用户名，用户角色，用户密码哈希值'''

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128), nullable=False, unique=True)
    nick_name = db.Column(db.String(128), nullable=False)
    user_password_hash = db.Column(db.String(128), nullable=False)

    id_unit = db.Column(db.Integer, db.ForeignKey('unit.id'))
    id_role = db.Column(db.Integer, db.ForeignKey('role.id'))

    def to_json(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'nick_name': self.nick_name
        }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.user_password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password_hash, password)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions ) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def get_teacher(self):
        pass

    def __init__(self, user_name, nick_name):
        self.user_name = user_name
        self.nick_name = nick_name

    def __repr__(self):
        return self.user_name
