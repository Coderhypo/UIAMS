# coding=utf-8
from flask import render_template, session, redirect, url_for, request, jsonify
from ..models import Grade, Role, User, Unit, CompetitionProject, Major
from flask.ext.login import login_required

import os
import json
import xlrd
from werkzeug import secure_filename
from . import admin
from .. import db

ALLOWED_EXTENSIONS = set(['xls','xlsx'])
UPLOAD_FOLDER = 'app/static/uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@admin.route('/')
@login_required
def index():
    return render_template('/admin/index.html')

@admin.route('/grade')
@login_required
def grade():
    grades_data = Grade.query.order_by('id').all()
    return render_template('/admin/grade.html', grades_data = grades_data)

@admin.route('/unit')
@login_required
def unit():
    units = Unit.query.filter_by().order_by('id').all()
    print units[0].majors
    return render_template('/admin/unit.html', units = units)

@admin.route('/unit/department')
@login_required
def department():
    return render_template('/admin/unit_department.html')

@admin.route('/unit/department/_get')
@login_required
def getDepartment():
    id = request.args.get('Id')
    majors = Major.query.filter_by(id_acachemy=id).order_by('id').all()
    return jsonify({'majors': [ major.to_json() for major in majors] })

@admin.route('/grade/_update')
@login_required
def gradeUpdate():
    id = request.args.get('Id', type=int)
    newName = request.args.get('Name')
    return jsonify(status=2)

@admin.route('/grade/_delete')
@login_required
def gradeDelete():
    id = request.args.get('Id', type=int)
    return jsonify(status=2)

@admin.route('/major/_insert')
@login_required
def majorInsert():
    return render_template('/admin/major_insert.html')

@admin.route('/major/_update')
@login_required
def majorUpdate():
    id = request.args.get('Id', type=int)
    newName = request.args.get('Name')
    return jsonify(status=2)

@admin.route('/major/_delete')
@login_required
def majorDelete():
    id = request.args.get('Id', type=int)
    return jsonify(status=2)

@admin.route('/unit/_insert')
@login_required
def unitInsert():
    return render_template('/admin/unit_insert.html')

@admin.route('/unit/_update')
@login_required
def unitUpdate():
    id = request.args.get('Id', type=int)
    newName = request.args.get('Name')
    return jsonify(status=2)

@admin.route('/unit/_delete')
@login_required
def unitDelete():
    id = request.args.get('Id', type=int)
    return jsonify(status=2)

''' 用户管理'''

@admin.route('/teacher')
@login_required
def teacher():
    teacherRole = Role.query.filter_by(role_name=u'教师').first()
    teachers = User.query.filter_by(role=teacherRole).all()
    return render_template('/admin/teacher.html',teachers = teachers)

@admin.route('/unit_admin')
@login_required
def unitAdmin():
    unitAdminRole = Role.query.filter_by(role_name=u'单位管理员').first()
    unitAdmins = User.query.filter_by(role=unitAdminRole).all()
    return render_template('/admin/unit_admin.html',unitAdmins = unitAdmins)

@admin.route('/system_admin')
@login_required
def systemAdmin():
    adminRole = Role.query.filter_by(role_name=u'管理员').first()
    admins = User.query.filter_by(role=adminRole).all()
    return render_template('/admin/system_admin.html',admins = admins)

@admin.route('/teacher/_insert')
@login_required
def teacherInsert():
    return render_template('/admin/teacher_insert.html')
    
@admin.route('/competition')
@login_required
def competition():
    competitionProject = CompetitionProject.query.order_by('id').all()
    return render_template('/admin/competition.html',competitionProject=competitionProject)

@admin.route('/competition/project/_insert', methods=['GET','POST'])
@login_required
def projectInsert():
    if request.method == "POST":
        if request.form.get('projectName') == None: 
            file = request.files['file']
            if file and allowed_file(file.filename):
                file_url = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_url)
                xls = xlrd.open_workbook(file_url)
                table = xls.sheets()[0]
                for i in range(table.nrows):
                    projectName = table.row(i)[0].value.encode('utf-8')
                    if CompetitionProject.query.filter_by(project_name=projectName).first() == None:
                        competitionProject = CompetitionProject(projectName)
                        db.session.add(competitionProject)
                db.session.commit()
            return redirect(url_for('.competition'))
        else:
            projectName = request.form['projectName']
            if CompetitionProject.query.filter_by(project_name=projectName).first() == None:
                competitionProject = CompetitionProject(projectName)
                db.session.add(competitionProject)
                db.session.commit()
            return redirect(url_for('.competition'))

    return render_template('/admin/competition_project_insert.html')
