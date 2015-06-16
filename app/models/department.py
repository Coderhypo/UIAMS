#-*- coding: utf-8 -*-

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
    teachers = db.relationship('User', backref='unit',lazy='dynamic')

    def department_to_json(self):
        return {
            'id': self.id,
            'acachemy': self.unit_name,
            'acachemy_id': self.unit_id,
            'majors': [{
                'major_id': major.id,
                'major_name': major.major_name
            } for major in self.majors]
        }

    def unit_teacher_to_json(self):
        return {
            'id': self.id,
            'unit_name': self.unit_name,
            'teachers': [{
                    'teacher_id': teacher.id ,
                    'teacher_name': teacher.nick_name + '/' + teacher.user_name
                } for teacher in self.teachers
            ]
        }

    def __init__(self, unit_id, unit_name):
        self.unit_id = unit_id
        self.unit_name = unit_name

    def __repr__(self):
        return self.unit_name

class Major(db.Model):

    '''学院专业表，字段包括：
    专业名称，专业所在学院'''

    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    major_id = db.Column(db.String(128), unique = True)
    major_name = db.Column(db.String(128))
    id_acachemy = db.Column(db.Integer, db.ForeignKey('unit.id'))

    def to_json(self):
        return {
            'id': self.major_id,
            'major_name': self.major_name
        }

    def __init__(self, major_id, major_name):
        self.major_id = major_id
        self.major_name = major_name

    def __repr__(self):
        return self.major_name
