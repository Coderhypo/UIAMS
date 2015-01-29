#-*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField, StringField, BooleanField, SelectField, FormField, DateField
from wtforms.validators import Required
from models import Acachemy, Teacher, ComName

def Aca_all():
    Aca = []
    for a in Acachemy.query.all():
        Aca.append((str(a.id),a.aca_name))
    return Aca

def Tea_all():
    Tea_name = []
    for t in Teacher.query.all():
        tea = t.tea_name + ' ' + t.tea_unit
        Tea_name.append((str(t.id),tea))
    return Tea_name

def Com_all():
    Com = []
    for c in ComName.query.all():
        Com.append((str(c.id), c.com_name))
    return Com

class BaseForm(Form):
    LANGUAGES = ['zh']

class LoginForm(BaseForm):
    userid = StringField(u'帐号', validators=[Required()])
    passwd = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登入')
   
class StuForm(BaseForm):
    stuid = StringField(u'学号', validators=[Required()])
    stuname = StringField(u'姓名', validators=[Required()])
    stuaca = SelectField(u'学院', choices=Aca_all())
    stumajor = StringField(u'专业', validators=[Required()])
    stuclass = StringField(u'班级', validators=[Required()])

class TeaForm(BaseForm):
    teaid1 = SelectField(u'教师工号1', choices=Tea_all())
    teaid2 = SelectField(u'教师工号2', choices=Tea_all())

class ComForm(BaseForm):
    comname = SelectField(u'竞赛项目', choices=Com_all())
    proname = StringField(u'成果名称')
    comlevel = SelectField(u'获奖级别', choices=[
            (u'省级',u'省级'), 
            (u'国家级',u'国家级'), 
            (u'亚洲区级',u'亚洲区级'), 
            (u'国际',u'国际')], validators=[Required()])
    comclass = SelectField(u'等级', choices=[
            (u'一等奖（金奖）',u'一等奖（金奖）'), 
            (u'二等奖（银奖）',u'二等奖（银奖）'), 
            (u'三等奖（铜奖）',u'三等奖（铜奖）')], validators=[Required()])
    comdate = DateField(u'获奖时间', validators=[Required()])
    comorg = StringField(u'颁奖单位', validators=[Required()])

class TeamForm(BaseForm):
    commain = FormField(ComForm,u'竞赛信息')
    comstu1 = FormField(StuForm, u'参赛学生1') 
    comstu2 = FormField(StuForm, u'参赛学生2') 
    comstu3 = FormField(StuForm, u'参赛学生3') 
    comstu4 = FormField(StuForm, u'参赛学生4') 
    comstu5 = FormField(StuForm, u'参赛学生5') 
    comtea = FormField(TeaForm, u'指导老师')
    submit = SubmitField(u'提交')

class PatentForm(BaseForm):
    peaname = StringField(u'实用新型名称:')
    inventor = StringField(u'发明人:')
    filingdate = StringField(u'专利申请日')
    patentee = StringField(u'专利权人')
    announcement = StringField(u'授权公告日')
    submit = SubmitField(u'提交')


class PerForm(TeaForm, ComForm, StuForm):
    submit = SubmitField(u'提交')

