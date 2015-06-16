# coding=utf-8
from flask import render_template, redirect, url_for, request, current_app
from ..models import Project, Unit, Competition, Adviser, Participant, Grade
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
        achievement_name = request.form['achievement_name']
        winning_level = request.form['winning_level']
        rate = request.form['rate']
        winning_time = request.form['winning_time']
        awards_unit = request.form['awards_unit']

        competition = Competition(achievement_name, winning_level, rate, awards_unit,winning_time)
        competition.id_project = request.form['project']

        db.session.add(competition)
        db.session.commit()

        adviser_1 = Adviser(1)
        adviser_1.id_competition = competition.id
        adviser_1.id_teacher = request.form['teacher1']

        adviser_2 = Adviser(2)
        adviser_2.id_competition = competition.id
        adviser_2.id_teacher = request.form['teacher2']

        db.session.add_all([adviser_1, adviser_2])
        db.session.commit()

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
    return 'hello world'

@app.route('/competition/<int:id>/participant', methods=['GET', 'POST'])
@login_required
def participant(id):
    participants = Competition.query.filter_by(id=id).first()
    if participants:
        return redirect(url_for('show_competition', id=id))
    grades = Grade.query.all()
    return render_template('/competition/participant.html', grades = grades)
