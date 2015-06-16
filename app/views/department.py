#-*- coding: utf-8 -*-
from flask import request, jsonify
from ..models import Major, Unit
from flask.ext.login import login_required

import json
from .. import db, app

@app.route('/department/_get')
@login_required
def getDepartment():
    units = Unit.query.all()
    return jsonify({'departments': [ unit.department_to_json() for unit in units] })
