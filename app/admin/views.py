# coding=utf-8
from flask import render_template, session, redirect, url_for, request, jsonify
from ..models import Acachemy, Grade

from . import admin
from .. import db

@admin.route('/')
def index():
    return render_template('/admin/index.html')

@admin.route('/grade')
def acachemy():
    grades_data = Grade.query.order_by('id').all()
    return render_template('/admin/grade.html', grades_data = grades_data)

@admin.route('/department')
def department():
    departments_data = Acachemy.query.order_by('id').all()
    return render_template('/admin/department.html', department_data = departments_data)

@admin.route('/major/_remove')
def majorRemove():
    id = request.args.get('Id', type=int)
    print id
    return jsonify(status=2)

@admin.route('/major/_edit')
def majorEdit():
    id = request.args.get('Id', type=int)
    newName = request.args.get('Name')
    print id, newName
    return jsonify(status=2)

@admin.route('/acachemy/_remove')
def acachemyRemove():
    id = request.args.get('Id', type=int)
    print id
    return jsonify(status=2)

@admin.route('/acachemy/_edit')
def acachemyEdit():
    id = request.args.get('Id', type=int)
    newName = request.args.get('Name')
    print id, newName
    return jsonify(status=2)

