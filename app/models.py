from app import db
from datetime import datetime

class ComName(db.Model):
    __tablename__ = 'comname'
    id = db.Column(db.Integer, primary_key=True)
    com_name = db.Column(db.String(24), nullable=False)

    def __init__(self, com_name):
        self.com_name=com_name

class ComInfo(db.Model):
    __tablename__ = 'cominfo'
    id = db.Column(db.Integer, primary_key=True)
    com_nid = db.Column(db.Integer, db.ForeignKey('comname.id'), nullable=False)
    pro_name = db.Column(db.String(24), nullable=True)
    com_level = db.Column(db.Integer, nullable=False)
    com_class = db.Column(db.Integer, nullable=False)
    com_sid = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'), nullable=True)
    com_tid = db.Column(db.Integer, db.ForeignKey('comteam.team_id'), nullable=True)
    tea1_id = db.Column(db.Integer, db.ForeignKey('comtea.tea_id'), nullable=False)
    tea2_id = db.Column(db.Integer, db.ForeignKey('comtea.tea_id'), nullable=False)
    com_time = db.Column(db.Date, nullable=False)
    com_org = db.Column(db.String(10), nullable=False)
    is_team  = db.Column(db.Integer, nullable=False)

    def __init__(self, com_nid, pro_name, com_level, com_class, tea1_id, tea2_id, com_org, is_team, com_sid=None, com_tid=None, com_time=None):
        self.com_nid=com_nid
        self.pro_name=pro_name
        self.com_level=com_level
        self.com_class=com_class
        self.com_org=com_org
        self.tea1_id=tea1_id
        self.tea2_id=tea2_id
        
        if is_team == True:
            self.com_tid=com_tid
        else:
            self.com_sid=com_sid
            
        if com_time == None:
            self.com_time = datetime.utcnow()

class ComTeam(db.Model):
    __tablename__ = 'comteam'
    team_id = db.Column(db.Integer, primary_key=True)
    stu1_id = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'), nullable=False)
    stu2_id = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'))
    stu3_id = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'))
    stu4_id = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'))
    stu5_id = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'))
    stu6_id = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'))
    stu7_id = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'))
    stu8_id = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'))
    stu9_id = db.Column(db.Integer, db.ForeignKey('comstu.stu_id'))

    def __init__(self):
        pass

class ComStu(db.Model):
    __tablename__ = 'comstu'
    stu_id = db.Column(db.Integer, primary_key=True, nullable=False)
    stu_academy = db.Column(db.String(10), nullable=False)
    stu_major = db.Column(db.String(10), nullable=False)
    stu_class = db.Column(db.String(10), nullable=False)
    
    def __init__(self, stu_id, stu_academy, stu_major, stu_class):
        self.stu_id=stu_id
        self.stu_academy=stu_academy
        self.stu_major=stu_major
        self.stu_class=stu_class
       
class ComTea(db.Model):
    __tablename__ = 'comtea'
    tea_id = db.Column(db.Integer, primary_key=True)
    tea_academy = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    
    def __init__(self, tea_id, tea_academy, password):
        self.tea_id=tea_id
        self.tea_academy=tea_academy
        self.password=password

class ComAca(db.Model):
    __tablename__ = 'comaca'
    aca_id = db.Column(db.Integer, primary_key=True)
    aca_name = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    
    def __init__(self, aca_name, password):
        self.aca_name=aca_name
        self.password=password
