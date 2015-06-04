#-*- coding: utf-8 -*-
from ..models import Unit
from ..models import Grade
from .mixin import ModelViewMixin, BaseViewMixin
from flask.ext.admin import expose, expose_plugview
from .. import db
from . import admin
from flask import views

class DepartmentAdmin(ModelViewMixin):

    can_restore = False
    can_create = True
    can_edit = False
    can_delete = True

    column_searchable_list = ['unit_name']

    list_template = 'admin/department.html'

    def __init__(self, session, **kwargs):
        super(DepartmentAdmin, self).__init__(Unit, session, **kwargs)

class GradeAdmin(ModelViewMixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = ['grade_name']

    column_list = ('id', 'grade_name')

    def __init__(self, session, **kwargs):
        super(GradeAdmin, self).__init__(Grade, session, **kwargs)

admin.add_view(DepartmentAdmin(db.session, category=u'信息管理', name=u'院系信息',
    endpoint='department'))
admin.add_view(GradeAdmin(db.session, category=u'信息管理', name=u'年级信息'))
