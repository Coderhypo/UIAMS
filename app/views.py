#-*- coding: UTF-8 -*-
from app import db, app, login_manager
from flask import render_template, redirect, request, url_for, flash, session
from flask.ext.login import login_user, login_required, logout_user, current_user
from models import Role, User, Student, Acachemy, Teacher, CompetitionInfo, CompetitionName
from forms import LoginForm, ComTeamForm, CompetitionIndividualForm, CreateUserForm, DeleteUserForm, UpdateUserForm, CreateTeacherForm, RetrieveTeacherForm, DeleteTeacherForm, UpdateTeacherForm, CreateAcachemyForm, DeleteAcachemyForm, UpdateAcachemyForm, PatentForm
from decorators import commit_required, query_required

@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('competition.html')  

@app.route('/individual_com', methods=['GET', 'POST'])
@login_required
def individual_com():
    form = CompetitionIndividualForm()
    form.acachemys.query = Acachemy.query.all()
    form.teachers1.query = Teacher.query.all()
    form.teachers2.query = Teacher.query.all()
    form.competitions_name.query = CompetitionName.query.all()

    if request.method=='POST' and form.validate():
        competitions_name = form.competitions_name.data
        student = Student.query.filter_by(stu_id=form.student_id.data).first()
        acachemy = form.acachemys.data
        teacher1 = form.teachers1.data
        teacher2 = form.teachers2.data

        if student == None:
            student = Student(
                stu_id = form.student_id.data,
                stu_name = form.student_name.data,
                stu_major = form.student_major.data,
                stu_class = form.student_class.data
            )
            student.acachemy = acachemy
            
            db.session.add(student)
            db.session.commit()

        competition_info = CompetitionInfo(
            pro_name = form.project_name.data,
            com_level = form.competition_level.data,
            com_class = form.competition_class.data,
            com_org = form.competition_org.data,
            com_time = form.competition_date.data,
            com_sid = student.id,
            tea1_id = teacher1.id,
            tea2_id = teacher2.id,
            is_team = 0
        )
        competition_info.com_name = competitions_name

        db.session.add(competition_info)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('individual_com.html', form=form)


@app.route('/patent',methods=['GET','POST'])
@login_required
def patent():
    form = PatentForm()
    if request.method == 'POST':
            Pat_info = Patent.query.filter_by(pea_name = form.peaname.data).first()
            if Pat_info == None: 
                '''
                Pat_info = Patent(
                    pea_type = form.type.data,
                    pea_name = form.peaname.data,
                    pea_inventor = form.inventor.data,
                    pea_filingdate = form.filingdate.data,
                    pea_patentee = form.patentee.data,
                    pea_announcement = form.announcement.data
                )
            
                db.session.add(Pat_info)
                db.session.commit()
                '''
            return redirect (url_for('index'))
    return render_template('patent.html',form = form)
    

@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html")


@app.route('/admin/user', methods=['GET', 'POST'])
@login_required
def admin_user():

    create_form = CreateUserForm()
    create_form.roles.query = Role.query.all()

    delete_form = DeleteUserForm()
    delete_form.users.query = User.query.all()

    update_form = UpdateUserForm()
    update_form.users.query = User.query.all()
    update_form.roles.query = Role.query.all()

    if request.method == 'POST':
        if create_form.data['create'] and create_form.validate():
            form = create_form
            user = User.query.filter_by(user_id=form.create_id.data).first()
            role = form.roles.data
            
            if user == None:
                user = User(
                    user_id=form.create_id.data,
                    user_name=form.create_name.data)
                user.password = '123456'
                user.role = role

            db.session.add(user)
            db.session.commit()
            
            session['status'] = u'success'
            flash(u'成功添加登录用户信息!')
            return redirect(url_for('admin_user'))
        elif delete_form.data['delete'] and delete_form.validate():
            form = delete_form
            user = form.users.data
            
            db.session.delete(user)
            db.session.commit()
            
            session['status'] = u'warning'
            flash(u'成功删除登录用户信息!')
            return redirect(url_for('admin_user'))
        elif update_form.data['update'] and update_form.validate():
            form = update_form
            user = form.users.data
            role = form.roles.data
            name = form.update_name.data
            password = form.update_passwd.data
            user.role = role
            
            if password != '':
                user.password = password
            elif name != '':
                user.user_name = name
            
            db.session.add(user)
            db.session.commit()
            
            session['status'] = u'info'
            flash(u'成功修改登录用户信息!')
            return redirect(url_for('admin_user'))

    return render_template('admin-user.html', create_form=create_form, delete_form=delete_form, update_form=update_form)

@app.route('/admin/teacher', methods=['GET', 'POST'])
@login_required
def admin_teacher():

    create_form = CreateTeacherForm()

    retrieve_form = RetrieveTeacherForm()
    retrieve_form.teachers.query = Teacher.query.all()

    update_form = UpdateTeacherForm()
    update_form.teachers.query = Teacher.query.all()

    delete_form = DeleteTeacherForm()
    delete_form.teachers.query = Teacher.query.all()

    if request.method=='POST':
        if create_form.data['create'] and create_form.validate():
            form = create_form
            teacher = Teacher.query.filter_by(tea_id=form.create_id.data).first()
            
            if teacher == None:
                teacher = Teacher(
                    tea_id=form.create_id.data,
                    tea_name=form.create_name.data,
                    tea_unit=form.create_unit.data
                )
            
            db.session.add(teacher)
            db.session.commit()
            
            session['status'] = 'success'
            flash(u'成功添加教师信息!')
            return redirect(url_for('admin_teacher'))
        elif retrieve_form.data['retrieve'] and retrieve_form.validate():
            form = retrieve_form
            teacher = form.teachers.data
            print teacher
            
            return render_template('admin-teacher.html', create_form=create_form, retrieve_form=retrieve_form, delete_form=delete_form, update_form=update_form, teacher=teacher)
        elif update_form.data['update'] and update_form.validate():
            form = update_form
            teacher = form.teachers.data
            name = form.update_name.data
            unit = form.update_unit.data
            
            if name != '':
                teacher.tea_name = name
            
            if unit !='':
                teacher.tea_unit = unit

            db.session.add(teacher)
            db.session.commit()

            session['status'] = u'info'
            flash(u'成功修改教师信息!')
            return redirect(url_for('admin_teacher'))
        elif delete_form.data['delete'] and delete_form.validate():
            form = delete_form
            teacher = form.teachers.data
            
            db.session.delete(teacher)
            db.session.commit()
            
            session['status'] = 'warning'
            flash(u'成功删除教师信息!')
            return redirect(url_for('admin_teacher'))
    return render_template('admin-teacher.html',
            create_form=create_form, 
            retrieve_form=retrieve_form,
            delete_form=delete_form, 
            update_form=update_form
        )

@app.route('/admin/acachemy', methods=['GET', 'POST'])
@login_required
def admin_acachemy():

    create_form = CreateAcachemyForm()

    delete_form = DeleteAcachemyForm()
    delete_form.acachemys.query = Acachemy.query.all() 

    update_form = UpdateAcachemyForm()
    update_form.acachemys.query = Acachemy.query.all()

    if request.method=='POST':
        if create_form.data['create'] and create_form.validate():
            form = create_form
            acachemy = Acachemy.query.filter_by(aca_name=form.create_name.data).first()
            
            if acachemy == None:
                acachemy = Acachemy(aca_name=form.create_name.data)
            
            db.session.add(acachemy)
            db.session.commit()
            
            session['status'] = u'success' 
            flash(u'成功添加学院信息!')
            return redirect(url_for('admin_acachemy'))
        elif delete_form.data['delete'] and delete_form.validate():
            form = delete_form
            acachemy = form.acachemys.data
            
            db.session.delete(acachemy)
            db.session.commit()
            
            session['status'] = 'warning'
            flash(u'成功删除学院信息!')
            return redirect(url_for('admin_acachemy'))
        elif update_form.data['update'] and update_form.validate():
            form = update_form
            acachemy = form.acachemys.data
            name = form.update_name.data

            if name != '':
                acachemy.aca_name = name
            
            db.session.add(acachemy)
            db.session.commit()
            
            status = u'info'
            session['status'] = u'info'
            flash(u'成功修改学院信息!')
            return redirect(url_for('admin_acachemy'))
    return render_template('admin-acachemy.html',
            create_form=create_form, 
            delete_form=delete_form, 
            update_form=update_form
        )

@app.route('/admin/competition', methods=['GET', 'POST'])
@login_required
def admin_competition():
    return render_template('admin-competition.html')
