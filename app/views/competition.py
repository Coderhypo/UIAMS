# coding=utf-8
from flask import render_template, redirect, url_for, request, current_app
from ..models import (
        Project,
        Unit,
        Competition,
        Adviser,
        Participant,
        Grade,
        Student
    )
from flask.ext.login import login_required

from .. import app, db
import os
from werkzeug import secure_filename

ALLOWED_EXTENSIONS = set(['jpg'])
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/competition', methods=['GET', 'POST'])
@login_required
def competition():
    projects = Project.query.order_by('id').all()
    if request.method == "POST":
        try:
            teacher_num = int(request.form['teacher_num'])
            achievement_name = request.form['achievement_name']
            winning_level = request.form['winning_level']
            rate = request.form['rate']
            winning_time = request.form['winning_time']
            awards_unit = request.form['awards_unit']

            competition = Competition(achievement_name, winning_level, rate, awards_unit,winning_time)
            competition.id_project = request.form['project']

            db.session.add(competition)

            for i in range(1, teacher_num + 1):
                adviser = Adviser(1)
                adviser.competition = competition
                adviser.id_teacher = request.form['No_%s_teacher' % i]

                db.session.add(adviser)

            db.session.commit()
        except:
            db.session.rollback()

        file = request.files['file']
        if file and allowed_file(file.filename):
            file.filename = 'competition_%s.jpg' % competition.id
            file_url = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_url)

        return redirect(url_for('participant', id=competition.id))

    return render_template('/competition/competition.html', projects=projects)

@app.route('/competition/<int:id>')
@login_required
def show_competition(id):
    competition = Competition.query.filter_by(id=id).first()
    return render_template('/competition/show_competition.html',
            competition=competition)

@app.route('/competition/<int:id>/participant', methods=['GET', 'POST'])
@login_required
def participant(id):
    competition = Competition.query.filter_by(id=id).first()
    if not competition:
        return redirect(url_for('competition'))
    elif competition.participants.all():
        return redirect(url_for('show_competition', id=id))
    grades = Grade.query.all()
    if request.method == 'POST':
        try:
            student_num = int(request.form['student_num'])
            for i in range(1, student_num + 1):
                student_id = request.form['No_%s_id' % i]
                student = Student.query.filter_by(student_id=student_id).first()
                if not student:
                    student_name = request.form['No_%s_name' % i]
                    student = Student(student_id, student_name)
                    student.id_grade = request.form['No_%s_grade' % i]
                    student.id_acachemy = request.form['No_%s_acachemy' % i]
                    student.id_major = request.form['No_%s_major' % i]
                    db.session.add(student)

                participant = Participant(i)
                participant.student = student
                participant.id_competition = id
                db.session.add(participant)

            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('show_competition', id=id))
    return render_template('/competition/participant.html', grades = grades)
