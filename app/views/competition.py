# coding=utf-8
from flask import render_template, session, redirect, url_for, request
from ..models import Project, Grade, Unit, Major, Student, User, Participants, Competition
from flask.ext.login import login_required

from .. import app, db
import os
from werkzeug import secure_filename

@app.route('/competition', methods=['GET', 'POST'])
@login_required
def competition():
    projects = Project.query.order_by('id').all()
    if request.method == "POST":
        achievement_name = request.form['achievement_name']
        winning_level = request.form['winning_level']
        rate = request.form['rate']
        winning_time = request.form['winning_time']
        awards_unit = request.form['awards_unit']

        competition = Competition(achievement_name, winning_level, rate, awards_unit,winning_time)
        competition.id_project = request.form['project']
        competition.id_teacher_1 = request.form['teacher1']
        competition.id_teacher_2 = request.form['teacher2']

        db.session.add(competition)
        db.session.commit()
        return render_template('/competition/competition.html', projects =projects)

    return render_template('/competition/competition.html', projects =projects)
