#-*- coding: UTF-8 -*-
from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin

@login_manager.user_loader
def load_user(id):
    return ComUser.query.get(int(id))

class Permission:
    ADMINISTER = 0x01
    COMMIT = 0x02
    QUERY = 0x04

class ComName(db.Model):
    __tablename__ = 'comname'
    id = db.Column(db.Integer, primary_key=True)
    com_name = db.Column(db.String(128), nullable=False)
    com_info = db.relationship('ComInfo', backref='name', lazy='dynamic') 

    def __init__(self, com_name):
        self.com_name=com_name

    def __repr__(self):
        return '<ComName %s>' % self.com_name
        
    @staticmethod
    def insert_cname():
        Comname=[u'国际大学生数学建模竞赛', 
        u'第39届ACM国际大学生程序设计竞赛亚洲区域赛（西安）', 
        u'第39届ACM国际大学生程序设计竞赛上海邀请赛暨2014全国大学生程序设计竞赛（上海）']
        for name in Comname:
            cn = ComName.query.filter_by(com_name=name).first()
            if cn is None:
                cn = ComName(com_name=name)
                db.session.add(cn)
        db.session.commit()
    
class ComInfo(db.Model):
    __tablename__ = 'cominfo'
    id = db.Column(db.Integer, primary_key=True)
    com_nid = db.Column(db.Integer, db.ForeignKey('comname.id'), nullable=False)
    pro_name = db.Column(db.String(128), nullable=True)
    com_level = db.Column(db.String(128), nullable=False)
    com_class = db.Column(db.String(128), nullable=False)
    com_sid = db.Column(db.Integer, db.ForeignKey('comstu.id'), nullable=True)
    com_tid = db.Column(db.Integer, db.ForeignKey('comteam.id'), nullable=True)
    tea1_id = db.Column(db.Integer, db.ForeignKey('comtea.id'), nullable=False)
    tea2_id = db.Column(db.Integer, db.ForeignKey('comtea.id'), nullable=False)
    com_time = db.Column(db.Date, nullable=False)
    com_org = db.Column(db.String(128), nullable=False)
    is_team  = db.Column(db.Integer, nullable=False)

    def __init__(self, com_nid, pro_name, com_level, com_class, tea1_id, tea2_id, com_time, com_org, is_team):
        self.com_nid=com_nid
        self.pro_name=pro_name
        self.com_level=com_level
        self.com_class=com_class
        self.com_org=com_org
        self.com_time = com_time
        self.tea1_id=tea1_id
        self.tea2_id=tea2_id
        self.is_team = is_team
        
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
    stu_id = db.Column(db.String(128), nullable=False, unique=True)
    stu_name = db.Column(db.String(128), nullable=False)
    stu_academy = db.Column(db.Integer, db.ForeignKey('comaca.id'), nullable=False)
    stu_major = db.Column(db.String(128), nullable=False)
    stu_class = db.Column(db.String(128), nullable=False)
    
    def __init__(self, stu_id, stu_name, stu_academy, stu_major, stu_class):
        self.stu_id=stu_id
        self.stu_name=stu_name
        self.stu_academy=stu_academy
        self.stu_major=stu_major
        self.stu_class=stu_class
       
    def __repr__(self):
        return '<ComStu %s>' % self.stu_id

class ComTea(db.Model):
    __tablename__ = 'comtea'
    id = db.Column(db.Integer, primary_key=True)
    tea_id = db.Column(db.String(128), nullable=False, unique=True)
    tea_name = db.Column(db.String(128), nullable=False)
    tea_academy = db.Column(db.Integer, db.ForeignKey('comaca.id'), nullable=False)
    
    def __init__(self, tea_id, tea_name, tea_academy):
        self.tea_id=tea_id
        self.tea_name=tea_name
        self.tea_academy=tea_academy

    @staticmethod
    def insert_teas():
        Teas = [('1','nplus',1) ,                    
        ('2','Jun',3)]
        for t in Teas:
            tea = ComTea.query.filter_by(tea_id=t[0]).first()
            if tea is None:
                tea = ComTea(tea_id=t[0],tea_name=t[1],tea_academy=t[2])
                db.session.add(tea)
        db.session.commit()

class ComAca(db.Model):
    __tablename__ = 'comaca'
    id = db.Column(db.Integer, primary_key=True)
    aca_name = db.Column(db.String(128), nullable=False, unique=True)
    stus = db.relationship('ComStu', backref='stu', lazy='dynamic')
    teas = db.relationship('ComTea', backref='tea', lazy='dynamic')
    
    def __init__(self, aca_name):
        self.aca_name=aca_name
    
    def __repr__(self):
        return '<ComAca %r>' % self.aca_name

    @staticmethod
    def insert_acas():
        Acas = [u'机械工程学院',                        
        u'农业工程与食品科学学院',
        u'计算机科学与技术学院',
        u'建筑工程学院',
        u'材料科学与工程学院',
        u'理学院',
        u'文学与新闻传播学院',
        u'法学院',
        u'美术学院',
        u'体育学院',
        u'鲁泰纺织服装学院',
        u'交通与车辆工程学院',
        u'电气与电子工程学院',
        u'化学工程学院',
        u'资源与环境工程学院',
        u'命科学学院',
        u'商学院',
        u'外国语学院',
        u'马克思主义学院',
        u'音乐学院',
        u'国防教育学院'
        ]
        for a in Acas:
            aca = ComAca.query.filter_by(aca_name=a).first()
            if aca is None:
                aca = ComAca(aca_name=a)
                db.session.add(aca)
        db.session.commit()

class ComUser(UserMixin, db.Model):
    __tablename__ = 'comuser'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10), nullable=False, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('comroles.id'))
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, user_name, role_id):
        self.user_name = user_name
        self.role_id = role_id

    def __repr__(self):
        return '<ComUser %r>' % self.user_name

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions ) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissons):
        return False

    def is_administrator(self):
        return False

class ComRole(db.Model):
    __tablename__ = 'comroles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('ComUser', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<ComRole %r>' % self.name
    
    def __init__(self, name):
        self.name=name

    @staticmethod
    def insert_roles():
        roles = {
            'Teacher': (Permission.COMMIT, True),
            'Academy': (Permission.QUERY, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = ComRole.query.filter_by(name=r).first()
            if role is None:
                role = ComRole(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
        db.session.commit()
