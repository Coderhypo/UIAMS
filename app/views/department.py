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
    return jsonify({'department': [ unit.to_json() for unit in units] })

@app.route('/major/_get')
@login_required
def getMajor():
    id = request.args.get('Id')
    majors = Major.query.filter_by(id_acachemy=id).order_by('id').all()
    return jsonify({'majors': [ major.to_json() for major in majors] })
