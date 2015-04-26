#-*- coding: UTF-8 -*-
from app import db, login_manager
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

class CompetitionProject(db.Model):

    '''竞赛项目名称表'''

    __tablename__ = 'competitionproject'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(128), nullable=False)

    competitions = db.relationship('Competition', backref='competitionproject',lazy='dynamic')

    def __init__(self, project_name):
        self.project_name=project_name

    def __repr__(self):
        return '<ComName %r>' % self.project_name

class Participants(db.Model):

    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    id_student_1 = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    id_student_2 = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_student_3 = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_student_4 = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_student_5 = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_student_6 = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_student_7 = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_student_8 = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_student_9 = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_student_10 = db.Column(db.Integer, db.ForeignKey('student.id'))

class Competition(db.Model):

    __tablename__ = 'competition'
    id = db.Column(db.Integer, primary_key=True)
    id_competitionproject = db.Column(db.Integer, db.ForeignKey('competitionproject.id'))
    achievement_name = db.Column(db.String(128))
    winning_level = db.Column(db.String(128))
    rate = db.Column(db.String(128))
    awards_unit = db.Column(db.String(128))
    winning_time = db.Column(db.Date)
    id_student = db.Column(db.Integer, db.ForeignKey('student.id'))
    id_participants = db.Column(db.Integer, db.ForeignKey('participants.id'))
    id_teacher_1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_teacher_2 = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, achievement_name, winning_level, rate, awards_unit, winning_time):
        self.achievement_name = achievement_name
        self.winning_level = winning_level
        self.rate = rate
        self.awards_unit = awards_unit
        self.winning_time = winning_time

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
        return '<Student %r>' % self.student_id

class Unit(db.Model):

    '''学生学院表，字段包括：
    学院:名称'''

    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(128), nullable=False, unique=True)
    is_acachemy = db.Column(db.Integer, nullable=False, default=1)

    # 反向关系
    students = db.relationship('Student', backref='acachemy', lazy='dynamic')
    majors = db.relationship('Major', backref='acachemy', lazy='dynamic')
    unit = db.relationship('User', backref='unit',lazy='dynamic')

    def __init__(self, unit_name):
        self.unit_name=unit_name

    def __repr__(self):
        return '<Acachemy %r>' % self.unit_name

class Major(db.Model):

    '''学院专业表，字段包括：
    专业名称，专业所在学院'''

    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(128), nullable=False, unique=True)
    id_acachemy = db.Column(db.Integer, db.ForeignKey('unit.id'))

    def to_json(self):
        return {
            'id': self.id,
            'major_name': self.major_name
        }

    def __init__(self,id, major_name):
        self.id = id
        self.major_name = major_name

    def __repr__(self):
        return '<Major %r>' % self.major_name

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

class User(UserMixin, db.Model):

    '''用户表，字段包括：
    用户ID，用户名，用户角色，用户密码哈希值'''

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128), nullable=False, unique=True)
    nick_name = db.Column(db.String(128), nullable=False, unique=True)
    user_password_hash = db.Column(db.String(128), nullable=False)

    id_unit = db.Column(db.Integer, db.ForeignKey('unit.id'))
    id_role = db.Column(db.Integer, db.ForeignKey('role.id'))

    def to_json(self):
        return {
            'id': self.id,
            'user_name': self.user_name
        }

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.user_password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password_hash, password)

    def __init__(self, user_name, nick_name):
        self.user_name = user_name
        self.nick_name = nick_name

    def __repr__(self):
        return '<User %r>' % self.user_name

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


