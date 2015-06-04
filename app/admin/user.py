#-*- coding: utf-8 -*-
from flask import redirect, url_for, request, flash, views
from ..models import User
from ..models import Unit
from .mixin import ModelViewMixin, BaseViewMixin
from flask.ext.admin import expose_plugview
from .. import db
from . import admin

import os
import xlrd
from datetime import datetime
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['xls','xlsx'])
UPLOAD_FOLDER = '/tmp'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class UserAdmin(ModelViewMixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    list_template = 'admin/user.html'

    column_searchable_list = ['nick_name']

    column_list = ('id', 'user_name', 'nick_name', 'unit', 'role')

    column_filters = ['user_name', 'nick_name', Unit.unit_name, 'role']

    def __init__(self, session, **kwargs):
        super(UserAdmin, self).__init__(User, session, **kwargs)

class ImportTeacherView(BaseViewMixin):

    def is_visible(self):
        return False

    @expose_plugview('/')
    class ImportTeacher(views.MethodView):

        def post(self, cls):
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

admin.add_view(UserAdmin(db.session, category=u'用户管理', name=u'用户列表'))
admin.add_view(ImportTeacherView(url='import_teacher'))
