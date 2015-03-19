#-*- coding: UTF-8 -*-
import os
from app import create_app, db
from app.models import CompetitionName, User, Role, Major, Grade, Unit

def createdb():
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    print 'MANAGE: ', db
    db.drop_all()
    db.create_all()

    Role.insert_roles()
    admin_role = Role.query.filter_by(role_name='管理员').first()
    unitAdmin_role = Role.query.filter_by(role_name=u'单位管理员').first()
    teacher_role = Role.query.filter_by(role_name=u'教师').first()
    admin = User('admin', u'管理员')
    admin.password = '123'
    admin.role = admin_role

    grades = {
        '2011': u'2011级',
        '2012': u'2012级',
        '2013': u'2013级',
        '2014': u'2014级',
        '2015': u'2015级',
        '2016': u'2016级',
        '2017': u'2017级',
        '2018': u'2018级',
        '2019': u'2019级'
    }
    for g in grades:
        print grades[g]
        grade = Grade(g, grades[g])
        db.session.add(grade)
    db.session.commit()

    acas = {
    u'机械工程学院': [
        [u'材料成型及控制工程','080203'],
        [u'测控技术与仪器','080301']
    ],
    u'交通与车辆工程学院': [
        [u'车辆工程','080207']
    ],
    u'计算机科学与技术学院': [
        [u'计算机科学与技术','080901'],
        [u'软件工程','080902'],
        [u'数字媒体技术','080906']
    ],
    u'教务处':None
    } 
    for a in acas:
        print a
        aca = Unit(a)
        db.session.add(aca)
        aca = Unit.query.filter_by(unit_name=a).first()
        if acas[a] == None:
            aca.is_acachemy = 0
            db.session.commit()
            continue

        for i in acas[a]:
            major = Major(id=i[1],major_name=i[0])
            major.major_acachemy = aca.id
            db.session.add(major)
        db.session.commit()

    teachers = [
    ('050114', u'张先伟', u'计算机科学与技术学院'),
    ('110413', u'许敬', u'机械工程学院'),
    ('170518', u'巴奉丽', u'交通与车辆工程学院')]

    for t in teachers:
        tea = User(t[0],t[1])
        tea.role = teacher_role
        tea.password = '123'
        unit = Unit.query.filter_by(unit_name = t[2]).first()
        if unit == None:
            unit = Unit(t[2])
            db.session.add(unit)
            tea.unit = unit
        else :
            tea.unit = unit
        db.session.add(tea)
    db.session.commit()

if __name__ == '__main__':
    createdb()
