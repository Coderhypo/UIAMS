#-*- coding: utf-8 -*-
from ..models import User
from ..models import Unit
from .mixin import Mixin
from .. import db
from . import admin

class TeacherAdmin(Mixin):

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = ['nick_name']

    column_list = ('id', 'user_name', 'nick_name', 'unit', 'role')

    column_filters = ['user_name', 'nick_name', Unit.unit_name, 'role']

    def __init__(self, session, **kwargs):
        super(TeacherAdmin, self).__init__(User, session, **kwargs)

admin.add_view(TeacherAdmin(db.session, category=u'用户管理'))
