#-*- coding: UTF-8 -*-
from app import app, login_manager
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user, current_user
from models import ComName, ComUser, ComStu, ComAca, ComTea, ComInfo
from forms import LoginForm,TeamForm, PerForm
from decorators import commit_required, query_required
from app import db

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = ComUser.query.filter_by(user_name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/main')
@login_required
def main():
    return render_template("main.html")  
    

@app.route('/perinfo', methods=['GET', 'POST'])
@login_required
@commit_required
def perinfo():
    form = PerForm(request.form)
    if form.validate() and request.method=='POST':
        Cstu = ComStu.query.filter_by(stu_id=form.stuid.data).first()
        comn = ComName.query.filter_by(com_name=form.comname.data).first()
        tea1 = ComTea.query.filter_by(tea_id=form.teaid1.data).first()
        tea2 = ComTea.query.filter_by(tea_id=form.teaid2.data).first()
        if Cstu is None:
            aca_id = ComAca.query.filter_by(aca_name=form.stuaca.data).first().id
            Cstu = ComStu(
                stu_id=form.stuid.data,
                stu_name=form.stuname.data,
                stu_academy=aca_id,
                stu_major=form.stumajor.data,
                stu_class=form.stuclass.data)
            db.session.add(Cstu)
            db.session.commit()
        Cinfo = ComInfo(
            com_nid = comn.id,
            pro_name = form.proname.data,
            com_level = form.comlevel.data,
            com_class = form.comclass.data,
            com_time = form.comdate.data,
            com_org = form.comorg.data,
            tea1_id = tea1.id,
            tea2_id = tea2.id,
            is_team = 0,
            )
        Cinfo.com_sid = Cstu.id
        db.session.add(Cinfo) 
        db.session.commit()
    return render_template('perinfo.html', form=form)
    
@app.route('/teaminfo')
@login_required
def teaminfo():
    form = TeamForm(request.form)
    return render_template('teaminfo.html', form=form)  

@app.route('/query')
@login_required
@query_required
def query():
    return render_template('query.html')
