#-*- coding: UTF-8 -*-
from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Permission:
    
    '''权限设置'''
    
    ADMINISTER = 0x01
    COMMIT = 0x02
    QUERY = 0x04

class CompetitionName(db.Model):
    
    '''竞赛项目名称表'''
    
    __tablename__ = 'competitionname'
    id = db.Column(db.Integer, primary_key=True)
    competition_name = db.Column(db.String(128), nullable=False)

    def __init__(self, competition_name):
        self.competition_name=competition_name

    def __repr__(self):
        return '<ComName %r>' % self.competition_name
        
class CompetitionInfo(db.Model):
    
    __tablename__ = 'competitioninfo'
    id = db.Column(db.Integer, primary_key=True)

class Student(db.Model):
    
    '''学生信息表，字段包括：
    学生ID，学生姓名，学生所在学院，学生专业，学生所在年级'''
    
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(128), nullable=False, unique=True)
    student_name = db.Column(db.String(128), nullable=False)
    student_academy = db.Column(db.Integer, db.ForeignKey('acachemys.id'))
    student_major = db.Column(db.Integer, db.ForeignKey('majors.id'))
    student_class = db.Column(db.Integer, nullable=False)
    
    def __init__(self, student_id, student_name, student_class):
        self.student_id = student_id
        self.student_name = student_name
        self.student_class = student_class
       
    def __repr__(self):
        return '<Student %r>' % self.student_id

class Teacher(db.Model):
    
    '''教师信息表，字段包括：
    教师ID，教师姓名，教师所在单位'''
    
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(128), nullable=False, unique=True)
    teacher_name = db.Column(db.String(128), nullable=False)
    teacher_unit = db.Column(db.Integer, db.ForeignKey('units.id'))

    def __init__(self, teacher_id, teacher_unit):
        self.teacher_id=teacher_id
        self.teacher_name=teacher_name

    def __repr__(self):
        return '<Teacher %r>' % self.teacher_name

class Acachemy(db.Model):
    
    '''学生学院表，字段包括：
    学院名称'''
    
    __tablename__ = 'acachemys'
    id = db.Column(db.Integer, primary_key=True)
    acachemy_name = db.Column(db.String(128), nullable=False, unique=True)
    
    # 反向关系
    students = db.relationship('Student', backref='acachemy', lazy='dynamic')
    majors = db.relationship('Major', backref='acachemy', lazy='dynamic')
    
    def __init__(self, acachemy_name):
        self.acachemy_name=acachemy_name
    
    def __repr__(self):
        return '<Acachemy %r>' % self.acachemy_name

class Major(db.Model):
    
    '''学院专业表，字段包括：
    专业名称，专业所在学院'''

    __tablename__ = 'majors'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(128), nullable=False, unique=True)
    major_acachemy = db.Column(db.Integer, db.ForeignKey('acachemys.id'))
 
    def __init__(self,id, major_name):
        self.id = id
        self.major_name = major_name

    def __repr__(self):
        return '<Major %r>' % self.major_name

class Grade(db.Model):

    '''年级信息表，字段包括：
    年级编号，年级名称'''

    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    grade_name = db.Column(db.String(128), nullable=False, unique=True)
    
    def __init__(self, id, grade_name):
        self.id = id
        self.grade_name = grade_name

    def __repr__(self):
        return '<Grade %r>' % self.grade_name

class Unit(db.Model):
    
    '''教师单位表，字段包括：
    单位名称'''

    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, unit_name):
        self.unit_name = unit_name

    def __repr__(self):
        return '<Unit %r>' % self.unit_name

class User(UserMixin, db.Model):
    
    '''用户表，字段包括：
    用户ID，用户名，用户角色，用户密码哈希值'''
    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(128), nullable=False, unique=True)
    user_name = db.Column(db.String(128), nullable=False, unique=True)
    user_role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    user_password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.user_password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password_hash, password)
    
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.user_name = user_name

    def __repr__(self):
        return '<User %r>' % self.user_id

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions ) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissons):
        return False

    def is_administrator(self):
        return False

class Role(db.Model):
    
    '''角色表'''
    
    __tablename__ = 'roles'
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
            u'学院': (0xff),
            u'管理员': (0xff)
        }
        for r in roles:
            role = Role.query.filter_by(role_name=r).first()
            if role is None:
                role = Role(role_name=r)
                role.permissions = roles[r]
                db.session.add(role)
        db.session.commit()


