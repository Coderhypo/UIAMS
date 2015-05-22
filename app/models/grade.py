#-*- coding: UTF-8 -*-

from app import db

class Grade(db.Model):

    '''年级信息表，字段包括：
    年级编号，年级名称'''

    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True)
    grade_name = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, id, grade_name):
        self.id = id
        self.grade_name = grade_name

    def __repr__(self):
        return '<Grade %r>' % self.grade_name
