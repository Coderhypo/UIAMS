#!/usr/bin/env python2
# coding=utf-8
from flask import render_template, session, redirect, url_for

from . import competition
from .. import db

@competition.route('/individual')
def individual():
    return render_template('/competition/individual.html') 

@competition.route('/team')
def team():
    return render_template('/competition/team.html') 
