#-*- coding: UTF-8 -*-

from app import db

class Project(db.Model):

    '''竞赛项目名称表'''

    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(128), nullable=False)
    date_created = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )

    def __init__(self, project_name):
        self.project_name = project_name

    def __repr__(self):
        return self.project_name

    def to_json(self):
        return {
            'id': self.id,
            'project_name': self.project_name
        }

class Participant(db.Model):

    __tablename__ = 'participant'
    id = db.Column(db.Integer, primary_key=True)
    id_competition = db.Column(db.Integer, db.ForeignKey('competition.id'))
    id_student = db.Column(db.Integer, db.ForeignKey('student.id'))
    locant = db.Column(db.Integer)
    date_created = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )

    def __init__(self, locant):
        self.locant = locant

    def __repr__(self):
        return self.student.student_name

class Adviser(db.Model):

    __tablename__ = 'adviser'
    id = db.Column(db.Integer, primary_key=True)
    id_competition = db.Column(db.Integer, db.ForeignKey('competition.id'))
    id_teacher = db.Column(db.Integer, db.ForeignKey('user.id'))
    locant = db.Column(db.Integer)

    def __init__(self, locant):
        self.locant = locant

    def __repr__(self):
        return self.teacher.nick_name

class Competition(db.Model):

    __tablename__ = 'competition'
    id = db.Column(db.Integer, primary_key=True)
    id_project = db.Column(db.Integer, db.ForeignKey('project.id'))
    achievement_name = db.Column(db.String(128))
    winning_level = db.Column(db.String(128))
    rate = db.Column(db.String(128))
    awards_unit = db.Column(db.String(128))
    winning_time = db.Column(db.Date)
    is_review = db.Column(db.Boolean, default=False)
    date_created = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )

    project = db.relationship('Project', lazy=True)

    participants = db.relationship('Participant',
            foreign_keys=[Participant.id_competition],
            backref=db.backref('competition', lazy='joined'),
            lazy='dynamic',
            cascade='all, delete-orphan')

    advisers = db.relationship('Adviser',
            foreign_keys=[Adviser.id_competition],
            backref=db.backref('competition', lazy='joined'),
            lazy='dynamic',
            cascade='all, delete-orphan')

    def __init__(self, achievement_name, winning_level, rate, awards_unit, winning_time):
        self.achievement_name = achievement_name
        self.winning_level = winning_level
        self.rate = rate
        self.awards_unit = awards_unit
        self.winning_time = winning_time

