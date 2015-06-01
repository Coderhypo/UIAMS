#-*- coding: UTF-8 -*-
from flask import render_template, session, redirect, url_for, request,\
jsonify, current_app, flash
from ...models import Grade, Role, User, Unit, CompetitionProject, Major,\
Competition
from flask.ext.login import login_required

import os
import json
import xlrd
from datetime import datetime
from werkzeug import secure_filename
from .. import admin
from ... import db

ALLOWED_EXTENSIONS = set(['xls','xlsx'])
#UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
UPLOAD_FOLDER = '/tmp'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

''' 用户管理'''

@admin.route('/user/teacher')
@login_required
def teacher():
    teacherRole = Role.query.filter_by(role_name=u'教师').first()
    teachers = User.query.filter_by(role=teacherRole).order_by('id').all()
    return render_template('/admin/teacher_admin.html',teachers = teachers,
            error_message = None)

@admin.route('/teacher/_get')
@login_required
def teacherGet():
    id = request.args.get('Id', type=int)
    teacherRole = Role.query.filter_by(role_name=u'教师').first()
    teachers = User.query.filter_by(role=teacherRole, id_unit=id).all()
    return jsonify({'teachers': [teacher.to_json() for teacher in teachers ]})

@admin.route('/teacher/_delete')
@login_required
def teacherDelete():
    ids = tuple(int(x) for x in request.args.get('ids', type=str).split(','))
    try:
        db.session.query(User).\
            filter(User.id.in_(ids)).delete(synchronize_session=False)
    except:
        return jsonify(status=0)
    else:
        db.session.commit()
        return jsonify(status=1)

@admin.route('/teacher/_update')
@login_required
def teacherUpdate():
    id = request.args.get('id', type=int)
    new_name = request.args.get('newName')
    teacher = User.query.filter_by(id=id).first()
    teacher.nick_name = new_name
    db.session.add(teacher)
    db.session.commit()
    return jsonify(status=1)

@admin.route('/teacher/_insert', methods=['GET', 'POST'])
@login_required
def teacherInsert():
    if request.method == 'POST':
        utcnow = datetime.utcnow()
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.filename = utcnow.strftime('teachers_%Y-%m-%d(%H:%M:%S).xls')
            file_url = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_url)
            xls = xlrd.open_workbook(file_url)
            table = xls.sheets()[0]
            for i in range(1, table.nrows):
                try:
                    teacher_id = table.row(i)[0].value.encode('utf-8')
                    teacher_name = table.row(i)[1].value.encode('utf-8')

                    unit_id = int(table.row(i)[2].value.encode('utf-8'))
                    unit_name = table.row(i)[3].value.encode('utf-8')
                except:
                    flash(u'更新教师失败，错误数据格式第%s行'%i, 'danger')
                    db.session.rollback()
                    break

                teacher = User.query.filter_by(user_name = teacher_id,
                    nick_name = teacher_name).first()
                unit = Unit.query.filter_by(unit_id = unit_id,
                    unit_name = unit_name).first()

                if not unit:
                    unit = Unit(unit_id=unit_id, unit_name=unit_name)
                    db.session.add(unit)

                if not teacher:
                    teacher = User(teacher_id, teacher_name)
                    teacher.role = \
                        Role.query.filter_by(role_name=u'教师').first()
                    teacher.password = '123'
                    teacher.unit = unit
                    db.session.add(teacher)

            else:
                try:
                    db.session.commit()
                    flash(u'更新教师成功', 'success')
                except:
                    db.session.rollback()
                    flash(u'更新教师失败，未知错误', 'danger')
        else:
            flash(u'更新教师失败，文件格式错误', 'danger')
        return redirect(url_for('.teacher'))

@admin.route('/user/unit_admin')
@login_required
def unitAdmin():
    unitAdminRole = Role.query.filter_by(role_name=u'单位管理员').first()
    unitAdmins = User.query.filter_by(role=unitAdminRole).all()
    return render_template('/admin/unit_admin.html',unitAdmins = unitAdmins)

@admin.route('/user/system_admin')
@login_required
def systemAdmin():
    adminRole = Role.query.filter_by(role_name=u'管理员').first()
    admins = User.query.filter_by(role=adminRole).all()
    return render_template('/admin/system_admin.html',admins = admins)
