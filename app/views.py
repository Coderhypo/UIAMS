#-*- coding: UTF-8 -*-
from app import db, app, login_manager
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user, current_user
from models import User, Student, Acachemy, Teacher, ComInfo, ComName
from forms import LoginForm,TeamForm, PerForm
from decorators import commit_required, query_required

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.userid.data).first()
        if user is not None and user.verify_password(form.passwd.data):
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

@app.route('/competition')
@login_required
def competition():
    return render_template("competition.html")  
    
@app.route('/individual_com', methods=['GET', 'POST'])
@login_required
@commit_required
def individual_com():
    form = PerForm()
    #if form.validate_on_submit():
    if form.validate() and request.method=='POST':
        Com_stu = Student.query.filter_by(stu_id=form.stuid.data).first()

        # 如果该学生不存在数据库

        if Com_stu is None:
            # 学生的关系对象模型

            Com_stu = Student(
                stu_id=form.stuid.data,
                stu_name=form.stuname.data,
                stu_academy=int(form.stuaca.data),
                stu_major=form.stumajor.data,
                stu_class=form.stuclass.data 
            )
            
            db.session.add(Com_stu)
            db.session.commit()
            Com_stu = Student.query.filter_by(stu_id=form.stuid.data).first()

        # 竞赛信息对象模型

        Com_info = ComInfo(
            com_nid = int(form.comname.data),
            pro_name = form.proname.data,
            com_level = form.comlevel.data,
            com_class = form.comclass.data,
            com_time = form.comdate.data,
            com_org = form.comorg.data,
            com_sid = Com_stu.id,
            tea1_id = int(form.teaid1.data),
            tea2_id = int(form.teaid2.data),
            is_team = 0,
        )

        db.session.add(Com_info) 
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('individual_com.html', form=form)
    
"""
@app.route('/team_com')
@login_required
def team_com():
    form = TeamForm(request.form)
    return render_template('team_com.html', form=form)  

@app.route('/query')
@login_required
@query_required
def query():
    return render_template('query.html')
"""
