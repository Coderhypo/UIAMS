#-*- coding: UTF-8 -*-
from flask import render_template, session, redirect, url_for, request,\
jsonify, current_app, flash
from ...models import Grade, Role, User, Unit, Project, Major,\
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

@admin.route('/competition')
@login_required
def competition():
    competitions = Competition.query.order_by('id').all()
    return render_template('/admin/competition.html', competitions =
            competitions)

@admin.route('/competition/show/<int:id>')
@login_required
def competitionShow(id):
    competition = Competition.query.filter_by(id=id).first()
    return render_template('/admin/competition_show.html', competition =
            competition)

@admin.route("/competition/_delete")
@login_required
def competitionDelete():
    ids = tuple(int(x) for x in request.args.get('ids', type=str).split(','))
    try:
        db.session.query(Competition).\
            filter(Competition.id.in_(ids)).delete(
                synchronize_session=False)
    except:
        return jsonify(status=0)
    else:
        db.session.commit()
        return jsonify(status=1)

@admin.route('/competition/project')
@login_required
def competition_project():
    projects = Project.query.order_by('id').all()
    return render_template('/admin/competition_project.html',competitionProjects=projects)

@admin.route('/competition/project/_insert', methods=['GET','POST'])
@login_required
def projectInsert():
    if request.method == "POST":
        utcnow = datetime.utcnow()
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.filename = utcnow.strftime('projects_%Y-%m-%d(%H:%M:%S).xls')
            file_url = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_url)
            xls = xlrd.open_workbook(file_url)
            table = xls.sheets()[0]
            for i in range(1, table.nrows):
                try:
                    project_name = table.row(i)[0].value.encode('utf-8')
                except:
                    flash(u'更新竞赛失败，错误数据格式第%s行'%i, 'danger')
                    db.session.rollback()
                    break

                competition_project = \
                    CompetitionProject.query.filter_by(project_name=project_name).first()
                if not competition_project:
                    competitionProject = CompetitionProject(project_name)
                    db.session.add(competitionProject)
            else:
                try:
                    db.session.commit()
                    flash(u'更新竞赛成功', 'success')
                except:
                    db.session.rollback()
                    flash(u'更新竞赛失败，未知错误', 'danger')
        else:
            flash(u'更新竞赛失败，文件格式错误', 'danger')
        return redirect(url_for('.competition_project'))

@admin.route('/competition/project/_update')
@login_required
def projectUpdate():
    id = request.args.get('id', type=int)
    new_name = request.args.get('newName')
    project = CompetitionProject.query.filter_by(id=id).first()
    project.project_name = new_name
    db.session.add(project)
    db.session.commit()
    return jsonify(status=1)

@admin.route("/competition/project/_delete")
@login_required
def projectDelete():
    ids = tuple(int(x) for x in request.args.get('ids', type=str).split(','))
    try:
        db.session.query(CompetitionProject).\
            filter(CompetitionProject.id.in_(ids)).delete(synchronize_session=False)
    except:
        return jsonify(status=0)
    else:
        db.session.commit()
        return jsonify(status=1)

@admin.route("/competition/project/_get")
@login_required
def projectGet():
    projects = CompetitionProject.query.order_by('id').all()
    return jsonify({'projects': [ project.to_json() for project in projects] })
