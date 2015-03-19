#-*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField, StringField, BooleanField, SelectField, FormField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, ValidationError
from flask.ext.login import current_user

class BaseForm(Form):

    '''支持中文表单的表单基类'''

    LANGUAGES = ['zh']

class LoginForm(BaseForm):

    '''登录的表单类'''

    username = StringField(u'用户名', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')
   
