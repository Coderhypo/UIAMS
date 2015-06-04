#-*- coding: UTF-8 -*-
import os
from app import db
from app.models import CompetitionProject, User, Role, Major, Grade, Unit

def createdb():
    db.drop_all()
    db.create_all()

    Role.insert_roles()
    admin_role = Role.query.filter_by(role_name='管理员').first()
    unitAdmin_role = Role.query.filter_by(role_name=u'单位管理员').first()
    teacher_role = Role.query.filter_by(role_name=u'教师').first()
    admin = User('admin', u'管理员')
    admin.password = '123'
    admin.role = admin_role

if __name__ == '__main__':
    createdb()
