#-*- coding: UTF-8 -*-

from app import db

class Unit(db.Model):

    '''学生学院表，字段包括：
    学院:名称'''

    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer)
    unit_name = db.Column(db.String(128))

    # 反向关系
    students = db.relationship('Student', backref='acachemy', lazy='dynamic')
    majors = db.relationship('Major', backref='acachemy', lazy='dynamic')
    unit = db.relationship('User', backref='unit',lazy='dynamic')

    def __init__(self, unit_id, unit_name):
        self.unit_id = unit_id
        self.unit_name = unit_name

    def __repr__(self):
        return '<Acachemy %r>' % self.unit_name
