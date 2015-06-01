#-*- coding: UTF-8 -*-

from app import db

class Student(db.Model):

    '''学生信息表，字段包括：
    学生ID，学生姓名，学生所在学院，学生专业，学生所在年级'''

    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(128), nullable=False, unique=True)
    student_name = db.Column(db.String(128), nullable=False)

    id_grade = db.Column(db.Integer, db.ForeignKey('grade.id'))
    id_acachemy = db.Column(db.Integer, db.ForeignKey('unit.id'))
    id_major = db.Column(db.Integer, db.ForeignKey('major.id'))

    competitions = db.relationship('Competition', backref='student', lazy='dynamic')

    def __init__(self, student_id, student_name, id_grade, id_acachemy, id_major):
        self.student_id = student_id
        self.student_name = student_name
        self.id_grade = id_grade
        self.id_acachemy = id_acachemy
        self.id_major = id_major

    def __repr__(self):
        return self.student_id
