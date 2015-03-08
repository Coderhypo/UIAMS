#!/usr/bin/env python2
# coding=utf-8
from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views

