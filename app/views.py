#-*- coding: UTF-8 -*-
from app import db, app, login_manager
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user, current_user
<<<<<<< HEAD
from models import User, Student, Acachemy, Teacher, ComInfo, ComName,Patent
from forms import LoginForm,TeamForm, PerForm,PatentForm
=======
from models import Role, User, Student, Acachemy, Teacher, ComInfo, ComName
from forms import LoginForm,TeamForm, PerForm, AddUserForm, DelUserForm, ReSetUserForm, AddTeaForm, DelTeaForm, ReSetTeaForm, AddAcaForm, DelAcaForm, ReSetAcaForm
>>>>>>> nplus/master
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

<<<<<<< HEAD
@app.route('/patent',methods=['GET','POST'])
@login_required
def patent():
    form = PatentForm()
    if request.method == 'POST':
        print '1'
        Pat_info = Patent(
            pea_name = form.peaname.data,
            pea_inventor = form.inventor.data,
            pea_filingdate = form.filingdate.data,
            pea_patentee = form.patentee.data,
            pea_announcement = form.announcement.data
        )
        print '2'

        db.session.add(Pat_info)
        db.session.commit()
        return redirect (url_for('index'))
    return render_template('patent.html',form = form)
    
"""
@app.route('/team_com')
@login_required
def team_com():
    form = TeamForm(request.form)
    return render_template('team_com.html', form=form)  
@app.route('/query')
=======
@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html")


@app.route('/admin/user', methods=['GET', 'POST'])
@login_required
def admin_user():
    add_form = AddUserForm()
    add_form.add_user_role.query = Role.query.all()
    del_form = DelUserForm()
    del_form.del_user_name.query = User.query.all()
    re_form =ReSetUserForm()
    re_form.re_user_name.query = User.query.all()
    re_form.re_user_role.query = Role.query.all()
    if request.method == 'POST':
        if add_form.data['add'] and add_form.validate():
            user = User.query.filter_by(user_id=add_form.add_user_id.data).first()
            role = add_form.add_user_role.data
            if user == None:
                user = User(user_id=add_form.add_user_id.data, user_name=add_form.add_user_name.data)
                user.password = '123456'
                user.role = role
                db.session.add(user)
                db.session.commit()
            return redirect(url_for('admin'))
        elif del_form.data['delete'] and del_form.validate():
            user = del_form.del_user_name.data
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('admin'))
        elif re_form.data['reset'] and re_form.validate():
            user = re_form.re_user_name.data
            role = re_form.re_user_role.data
            password = re_form.re_user_passwd.data
            user.role = role
            if password != '':
                user.password = password
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('admin'))
    return render_template('admin-user.html', add_form=add_form, del_form=del_form, re_form=re_form)

@app.route('/admin/teacher', methods=['GET', 'POST'])
@login_required
def admin_teacher():
    add_form = AddTeaForm()
    del_form = DelTeaForm()
    del_form.del_tea_id.query = Teacher.query.all()
    re_form = ReSetTeaForm()
    re_form.re_tea_id.query = Teacher.query.all()
    if request.method=='POST':
        if add_form.data['add'] and add_form.validate():
            teacher = Teacher.query.filter_by(tea_id=add_form.add_tea_id.data).first()
            if teacher == None:
                teacher = Teacher(tea_id=add_form.add_tea_id.data, tea_name=add_form.add_tea_name.data, tea_unit=add_form.add_tea_unit.data)
                db.session.add(teacher)
                db.session.commit()
            return redirect(url_for('admin'))
        elif del_form.data['delete'] and del_form.validate():
            teacher = del_form.del_tea_id.data
            db.session.delete(teacher)
            db.session.commit()
            return redirect(url_for('admin'))
        elif re_form.data['reset'] and re_form.validate():
            return redirect(url_for('admin'))
    return render_template("admin-teacher.html",add_form=add_form, del_form=del_form, re_form=re_form)

@app.route('/admin/acachemy', methods=['GET', 'POST'])
>>>>>>> nplus/master
@login_required
def admin_acachemy():
    add_form = AddAcaForm()
    del_form = DelAcaForm()
    re_form = ReSetAcaForm()
    if request.method=='POST':
        if add_form.validate():
            pass
        elif del_form.validate():
            print 'b'
        elif re_form.validate():
            print 'c'
            return redirect(url_for('admin'))
    return render_template("admin-acachemy.html",add_form=add_form, del_form=del_form, re_form=re_form)
