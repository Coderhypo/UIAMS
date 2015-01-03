from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin

@login_manager.user_loader
def load_user(id):
    return ComUser.query.get(int(id))

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
    com_sid = db.Column(db.Integer, db.ForeignKey('comstu.id'), nullable=True)
    com_tid = db.Column(db.Integer, db.ForeignKey('comteam.id'), nullable=True)
    tea1_id = db.Column(db.Integer, db.ForeignKey('comtea.id'), nullable=False)
    tea2_id = db.Column(db.Integer, db.ForeignKey('comtea.id'), nullable=False)
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
    id = db.Column(db.Integer, primary_key=True)
    stu1_id = db.Column(db.Integer, db.ForeignKey('comstu.id'), nullable=False)
    stu2_id = db.Column(db.Integer, db.ForeignKey('comstu.id'))
    stu3_id = db.Column(db.Integer, db.ForeignKey('comstu.id'))
    stu4_id = db.Column(db.Integer, db.ForeignKey('comstu.id'))
    stu5_id = db.Column(db.Integer, db.ForeignKey('comstu.id'))
    stu6_id = db.Column(db.Integer, db.ForeignKey('comstu.id'))
    stu7_id = db.Column(db.Integer, db.ForeignKey('comstu.id'))
    stu8_id = db.Column(db.Integer, db.ForeignKey('comstu.id'))
    stu9_id = db.Column(db.Integer, db.ForeignKey('comstu.id'))

    def __init__(self):
        pass

class ComStu(db.Model):
    __tablename__ = 'comstu'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    stu_id = db.Column(db.String(10), nullable=False, unique=True)
    stu_academy = db.Column(db.Integer, db.ForeignKey('comaca.id'), nullable=False)
    stu_major = db.Column(db.String(10), nullable=False)
    stu_class = db.Column(db.String(10), nullable=False)
    
    def __init__(self, stu_id, stu_academy, stu_major, stu_class):
        self.stu_id=stu_id
        self.stu_academy=stu_academy
        self.stu_major=stu_major
        self.stu_class=stu_class
       
class ComTea(db.Model):
    __tablename__ = 'comtea'
    id = db.Column(db.Integer, primary_key=True)
    tea_id = db.Column(db.String(10), nullable=False, unique=True)
    tea_name = db.Column(db.String(10), nullable=False)
    tea_academy = db.Column(db.Integer, db.ForeignKey('comaca.id'), nullable=False)
    
    def __init__(self, tea_id, tea_name, tea_academy):
        self.tea_id=tea_id
        self.tea_name=tea_name
        self.tea_academy=tea_academy

class ComAca(db.Model):
    __tablename__ = 'comaca'
    id = db.Column(db.Integer, primary_key=True)
    aca_name = db.Column(db.String(10), nullable=False)
    
    def __init__(self, aca_name):
        self.aca_name=aca_name

class ComUser(UserMixin, db.Model):
    __tablename__ = 'comuser'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10), nullable=False, unique=True)
    user_class = db.Column(db.Integer, nullable=False) 
    password_hash = db.Column(db.String(128), nullable=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, user_name, user_class):
        self.user_name = user_name
        self.user_class = user_class
