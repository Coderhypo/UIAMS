#-*- coding: UTF-8 -*-
from app import db, app, login_manager
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required, logout_user, current_user
from models import Role, User, Student, Acachemy, Teacher, ComInfo, ComName
from forms import LoginForm, ComTeamForm, ComIndivForm, AddUserForm, DelUserForm, ReSetUserForm, AddTeaForm, DelTeaForm, ReSetTeaForm, AddAcaForm, DelAcaForm, ReSetAcaForm
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
def individual_com():

    form = ComIndivForm()
    form.stu_acachemy.query = Acachemy.query.all()
    form.tea1.query = Teacher.query.all()
    form.tea2.query = Teacher.query.all()
    form.com_name.query = ComName.query.all()

    print '111'
    if form.validate() and request.method=='POST':
        print '11'
        comname = form.com_name.data
        student = Student.query.filter_by(stu_id=form.stu_id.data).first()
        teacher1 = form.tea1.data
        teacher2 = form.tea2.data

        print '1'
        if student == None:
            student = Student(
                stu_id = form.stu_id.data,
                stu_name = form.stu_name.data,
                stu_major = form.stu_major.data,
                stu_class = form.stu_class.data
            )
            student.acachemy = form.stu_acachemy.data
            db.session.add(student)
            db.session.commit()

        cominfo = ComInfo(
            pro_name = form.pro_name.data,
            com_level = form.com_level.data,
            com_class = form.com_class.data,
            com_org = form.com_org.data,
            com_time = form.com_date.data,
            com_sid = student.id,
            tea1_id = teacher1.id,
            tea2_id = teacher2.id,
            is_team = 0
        )
        cominfo.com_name = comname

        db.session.add(cominfo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('individual_com.html', form=form)

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
    del_form.del_user.query = User.query.all()

    re_form = ReSetUserForm()
    re_form.re_user.query = User.query.all()
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
            user = del_form.del_user.data
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('admin'))
        elif re_form.data['reset'] and re_form.validate():
            user = re_form.re_user.data
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
    del_form.del_tea.query = Teacher.query.all()

    re_form = ReSetTeaForm()
    re_form.re_tea.query = Teacher.query.all()

    if request.method=='POST':
        if add_form.data['add'] and add_form.validate():
            teacher = Teacher.query.filter_by(tea_id=add_form.add_tea_id.data).first()
            if teacher == None:
                teacher = Teacher(tea_id=add_form.add_tea_id.data, tea_name=add_form.add_tea_name.data, tea_unit=add_form.add_tea_unit.data)
                db.session.add(teacher)
                db.session.commit()
            return redirect(url_for('admin'))
        elif del_form.data['delete'] and del_form.validate():
            teacher = del_form.del_tea.data
            db.session.delete(teacher)
            db.session.commit()
            return redirect(url_for('admin'))
        elif re_form.data['reset'] and re_form.validate():
            teacher = re_form.re_tea.data
            name = re_form.re_tea_name
            unit = re_form.re_tea_unit
            if name != '':
                teacher.tea_name = name
            if unit !='':
                teacher.tea_unit = unit
            db.session.add(teacher)
            db.session.commit()
            return redirect(url_for('admin'))

    return render_template("admin-teacher.html",add_form=add_form, del_form=del_form, re_form=re_form)

@app.route('/admin/acachemy', methods=['GET', 'POST'])
@login_required
def admin_acachemy():

    add_form = AddAcaForm()

    del_form = DelAcaForm()
    del_form.del_aca.query = Acachemy.query.all() 

    re_form = ReSetAcaForm()
    re_form.re_aca.query = Acachemy.query.all()

    if request.method=='POST':
        if add_form.data['add'] and add_form.validate():
            acachemy = Acachemy.query.filter_by(aca_name=add_form.add_aca_name)
            if acachemy == None:
                acachemy = Acachemy(aca_name=add_form.add_aca_name)
                db.sessoin.add(acachemy)
                db.session.commit()
                return redirect(url_for('admin'))
        elif del_form.data['delete'] and del_form.validate():
            acachemy = del_form.del_aca.data
            db.session.delete(acachemy)
            db.session.commit()
            return redirect(url_for('admin'))
        elif re_form.data['reset'] and re_form.validate():
            acachemy = re_form.re_aca.data
            name = re_form.re_aca_name.data
            if name != '':
                acachemy.aca_name = name
            db.session.add(acachemy)
            db.session.commit()
            return redirect(url_for('admin'))

    return render_template("admin-acachemy.html",add_form=add_form, del_form=del_form, re_form=re_form)
