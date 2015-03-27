#!/usr/bin/env python2
# coding=utf-8
from flask import render_template, session, redirect, url_for
from ..models import CompetitionProject, Grade, Unit, Major

from . import competition
from .. import db
import os
from werkzeug import secure_filename

@competition.route('/individual')
def individual():
    competitionProjects = CompetitionProject.query.order_by('id').all()
    grades = Grade.query.order_by('id').all()
    acachemys = Unit.query.filter_by(is_acachemy=1).order_by('id').all()
    majors = Major.query.order_by('id').all()
    return render_template('/competition/individual.html',competitionProjects=competitionProjects, grades = grades, acachemys = acachemys, majors = majors) 

@competition.route('/team')
def team():
    return render_template('/competition/team.html') 
