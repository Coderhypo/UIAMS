#-*- coding: utf-8 -*-
from flask import redirect, url_for, request, flash, views
from ..models import Competition, CompetitionProject, Unit
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

labels = dict(
    competitionproject = u'竞赛项目',
    project_name = u'项目名称',
    achievement_name = u'成果名称',
    winning_level = u'获奖级别',
    rate = u'等级',
    awards_unit = u'颁奖单位',
    winning_time = u'获奖时间',
    student = u'学生'
    )

class CompetitionAdmin(ModelViewMixin):

    column_labels = labels

    can_restore = False
    can_create = False
    can_edit = True
    can_delete = True

    column_list = ('id', 'competitionproject','achievement_name', 'winning_level', 'rate',
            'awards_unit', 'winning_time', 'student')

    column_filters = ['student', 'achievement_name', 'winning_level', 'rate',
            'awards_unit', 'winning_time']

    def __init__(self, session, **kwargs):
        super(CompetitionAdmin, self).__init__(Competition, session, **kwargs)

class ProjectAdmin(ModelViewMixin):

    column_labels = labels

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    list_template = 'admin/competition_project.html'

    #column_searchable_list = ['nick_name']

    #column_list = ('id', 'user_name', 'nick_name', 'unit', 'role')

    #column_filters = ['user_name', 'nick_name', Unit.unit_name, 'role']

    def __init__(self, session, **kwargs):
        super(ProjectAdmin, self).__init__(CompetitionProject, session, **kwargs)

class ImportProjectView(BaseViewMixin):

    def is_visible(self):
        return False

    @expose_plugview('/')
    class ImportProject(views.MethodView):

        def post(self, cls):
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
            return redirect(url_for('admin.index'))

admin.add_view(CompetitionAdmin(db.session, category=u'竞赛管理',
    name=u'竞赛列表'))
admin.add_view(ProjectAdmin(db.session, category=u'竞赛管理', name=u'竞赛项目'))
admin.add_view(ImportProjectView(url='import_project'))
