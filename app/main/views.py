#!/usr/bin/env python2
# coding=utf-8
from flask import render_template, session, redirect, url_for, request, flash
from ..models import User
from flask.ext.login import login_user, login_required, logout_user

from . import main
from .. import db

@main.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(user_id = request.form['username']).first()
        if user is not None and user.verify_password(request.form['password']):
            login_user(user, request.form.get('remember_me'))
            return redirect('/')
        else:
            flash('Invalid username or password')
    return redirect('/')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect('/')

@main.route('/')
def index():
    return render_template('/main/index.html')

