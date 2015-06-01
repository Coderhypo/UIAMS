#-*- coding: utf-8 -*-
from ..models import Competition
from ..models import CompetitionProject
from ..models import Unit
from .mixin import Mixin
from .. import db
from . import admin

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

class CompetitionAdmin(Mixin):

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

class ProjectAdmin(Mixin):

    column_labels = labels

    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    #column_searchable_list = ['nick_name']

    #column_list = ('id', 'user_name', 'nick_name', 'unit', 'role')

    #column_filters = ['user_name', 'nick_name', Unit.unit_name, 'role']

    def __init__(self, session, **kwargs):
        super(ProjectAdmin, self).__init__(CompetitionProject, session, **kwargs)

admin.add_view(CompetitionAdmin(db.session, category=u'竞赛管理'))
admin.add_view(ProjectAdmin(db.session, category=u'竞赛管理'))
