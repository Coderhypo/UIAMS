#!/usr/bin/env python2
# coding=utf-8
from flask import Blueprint

patent = Blueprint('patent', __name__)

from . import views

