#-*- coding: utf-8 -*-
from ..models import Grade
from .mixin import ModelViewMixin
from flask.ext.admin import expose, expose_plugview
from .. import db
from . import admin
from flask import views

labels = dict(
    id = u'#',
    grade_name = u'年级'
    )

class GradeAdmin(ModelViewMixin):

    column_labels = labels

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = ['grade_name']

    column_list = ('id', 'grade_name')

    def __init__(self, session, **kwargs):
        super(GradeAdmin, self).__init__(Grade, session, **kwargs)

admin.add_view(GradeAdmin(db.session, category=u'信息管理', name=u'年级信息'))
