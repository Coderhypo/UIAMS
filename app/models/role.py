#-*- coding: UTF-8 -*-

from app import db

class Role(db.Model):

    '''角色表'''

    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.role_name

    def __init__(self, role_name):
        self.role_name = role_name

    @staticmethod
    def insert_roles():
        roles= {
            u'教师': (0xff),
            u'单位管理员': (0xff),
            u'管理员': (0xff)
        }
        for r in roles:
            role = Role.query.filter_by(role_name=r).first()
            if role is None:
                role = Role(role_name=r)
                role.permissions = roles[r]
                db.session.add(role)
        db.session.commit()
