# coding=utf-8
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

@admin.route('/department')
@login_required
def department():
    units = Unit.query.order_by('id').all()
    return render_template('/admin/department.html', units = units)

@admin.route('/department/_insert', methods=['GET', 'POST'])
@login_required
def insertDepartment():
    if request.method == 'POST':
        utcnow = datetime.utcnow()
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.filename = utcnow.strftime('department_%Y-%m-%d(%H:%M:%S).xls')
            file_url = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_url)
            xls = xlrd.open_workbook(file_url)
            table = xls.sheets()[0]
            for i in range(1, table.nrows):
                try:
                    unit_id = int(table.row(i)[0].value.encode('utf-8'))
                    unit_name = table.row(i)[1].value.encode('utf-8')
                    major_id = table.row(i)[2].value.encode('utf-8')
                    major_name = table.row(i)[3].value.encode('utf-8')
                except:
                    flash(u'更新院系失败，错误数据格式第%s行'%i, 'danger')
                    db.session.rollback()
                    break

                unit = Unit.query.filter_by(unit_id = unit_id,
                    unit_name = unit_name).first()
                major = Major.query.filter_by(major_id = major_id,
                    major_name = major_name).first()
                if not unit:
                    unit = Unit(unit_id, unit_name)
                    db.session.add(unit)

                if not major:
                    major = Major(major_id, major_name)
                    major.acachemy = unit
                    db.session.add(major)

            else:
                try:
                    db.session.commit()
                    flash(u'更新院系成功', 'success')
                except:
                    db.session.rollback()
                    flash(u'更新院系失败，未知错误', 'danger')

        else:
            flash(u'更新院系失败，文件格式错误', 'danger')
        return redirect(url_for('.department'))

@admin.route('/department/_get')
@login_required
def getDepartment():
    id = request.args.get('Id')
    majors = Major.query.filter_by(id_acachemy=id).order_by('id').all()
    return jsonify({'majors': [ major.to_json() for major in majors] })

