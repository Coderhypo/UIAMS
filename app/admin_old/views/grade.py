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

@admin.route('/grade')
@login_required
def grade():
    grades = Grade.query.order_by('id').all()
    return render_template('/admin/grade.html', grades = grades)

@admin.route('/grade/_update')
@login_required
def gradeUpdate():
    id = request.args.get('id', type=int)
    new_name = request.args.get('newName')
    grade = Grade.query.filter_by(id=id).first()
    grade.grade_name = new_name
    db.session.add(grade)
    db.session.commit()
    return jsonify(status=1)

@admin.route('/grade/_delete')
@login_required
def gradeDelete():
    ids = tuple(int(x) for x in request.args.get('ids', type=str).split(','))
    try:
        db.session.query(Grade).\
            filter(Grade.id.in_(ids)).delete(synchronize_session=False)
    except:
        return jsonify(status=0)
    else:
        db.session.commit()
        return jsonify(status=1)

