#-*- coding: UTF-8 -*-
from flask import render_template
from flask.ext.login import login_required

from .. import admin

@admin.route('/')
@login_required
def index():
    return render_template('/admin/index.html')

