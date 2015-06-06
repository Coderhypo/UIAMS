#-*- coding: utf-8 -*-
from flask import request, jsonify
from ..models import User, Unit
from flask.ext.login import login_required

import json
from .. import db, app

@app.route('/teacher/_get')
@login_required
def getTeacher():
    units = Unit.query.all()
    return jsonify({'unit_teachers': [ unit.unit_teacher_to_json() for unit in units] })

