#-*- coding: utf-8 -*-
from ..models import Unit
from ..models import Grade
from .mixin import Mixin
from .. import db
from . import admin

class UnitAdmin(Mixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = ['unit_name']

    column_list = ('unit_id', 'unit_name')

    def __init__(self, session, **kwargs):
        super(UnitAdmin, self).__init__(Unit, session, **kwargs)

class GradeAdmin(Mixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = ['grade_name']

    column_list = ('id', 'grade_name')

    def __init__(self, session, **kwargs):
        super(GradeAdmin, self).__init__(Grade, session, **kwargs)

admin.add_view(UnitAdmin(db.session, category=u'信息管理'))
admin.add_view(GradeAdmin(db.session, category=u'信息管理'))
