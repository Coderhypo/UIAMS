#!/usr/bin/env python2
# coding=utf-8
from flask import Blueprint

thesis = Blueprint('thesis', __name__)

from . import views

