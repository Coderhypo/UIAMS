#-*- coding: UTF-8 -*-

from app import db

class CompetitionProject(db.Model):

    '''竞赛项目名称表'''

    __tablename__ = 'competitionproject'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(128), nullable=False)

    competitions = db.relationship('Competition', backref='competitionproject',lazy='dynamic')

    def __init__(self, project_name):
        self.project_name=project_name

    def __repr__(self):
        return self.project_name

    def to_json(self):
        return {
            'id': self.id,
            'project_name': self.project_name
        }

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
