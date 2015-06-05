#-*- coding: utf-8 -*-
from flask import redirect, url_for, request, flash, views
from ..models import Unit, Major
from .mixin import ModelViewMixin, BaseViewMixin
from flask.ext.admin import expose_plugview
from .. import db
from . import admin
from flask import views

import os
import xlrd
from datetime import datetime
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['xls','xlsx'])
UPLOAD_FOLDER = '/tmp'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class DepartmentAdmin(ModelViewMixin):

    can_restore = False
    can_create = True
    can_edit = False
    can_delete = True

    column_searchable_list = ['unit_name']

    list_template = 'admin/department.html'

    def __init__(self, session, **kwargs):
        super(DepartmentAdmin, self).__init__(Unit, session, **kwargs)

class ImportUnitView(BaseViewMixin):

    def is_visible(self):
        return False

    @expose_plugview('/')
    class ImportUnit(views.MethodView):

        def post(self, cls):
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
            return redirect(url_for('admin.index'))

admin.add_view(DepartmentAdmin(db.session, category=u'信息管理', name=u'院系信息'))
admin.add_view(ImportUnitView(url='import_unit'))
