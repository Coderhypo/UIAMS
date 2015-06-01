#-*- coding: utf-8 -*-
from flask.ext.login import current_user
from flask.ext.admin.actions import action
from flask.ext.admin.contrib.sqla import ModelView

class Mixin(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated()
            and current_user.is_administrator())
    '''
    list_template = 'admin/list.html'
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'
    '''

    @action('delete', u'删除', u'确定删除选中吗')
    def action_delete(self, ids):
        super(Mixin, self).action_delete(ids)

