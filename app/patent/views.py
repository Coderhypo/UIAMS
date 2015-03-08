#!/usr/bin/env python2
# coding=utf-8
from flask import render_template, session, redirect, url_for

from . import patent
from .. import db

@patent.route('/')
def index():
    return 'hello world'

