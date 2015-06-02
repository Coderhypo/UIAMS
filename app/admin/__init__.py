#-*- coding: UTF-8 -*-
from flask.ext.admin import Admin, AdminIndexView as _AdminIndexView
from flask.ext.login import current_user

class AdminIndexView(_AdminIndexView):
    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_administrator())

admin = Admin(name = u'大学生创新活动管理系统',
    index_view=AdminIndexView(name=u'首页'),
    base_template='admin/base.html',
    template_mode='admin'
    )
#
from .user import *
from .info import *
from .competition import *
