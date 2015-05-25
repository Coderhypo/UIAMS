#!/usr/bin/env python2
# coding=utf-8
from flask import render_template, session, redirect, url_for

from . import thesis
from .. import db

@thesis.route('/')
def index():
    return 'hello world'

