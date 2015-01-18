#-*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField, StringField, BooleanField, SelectField, FormField, DateField
from wtforms.validators import Required
from models import ComAca, ComName

class BaseForm(Form):
    LANGUAGES = ['zh']

class LoginForm(BaseForm):
    username = StringField(u'帐号', validators=[Required()])
    password = PasswordField(u'密码', validators=[Required()])
    identity = SelectField(u'身份', choices=[
        (u'admin',u'管理员'), 
        (u'teacher',u'老师'), 
        (u'academy',u'学院')], 
    validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登入')
   
class StuForm(BaseForm):
    stuid = StringField(u'学号',validators=[Required()])
    stuname = StringField(u'姓名', validators=[Required()])
    stuaca = SelectField(u'学院', choices=[
            (u'机械工程学院', u'机械工程学院'),                       
            (u'农业工程与食品科学学院', u'农业工程与食品科学学院'),
            (u'计算机科学与技术学院', u'计算机科学与技术学院'),
            (u'建筑工程学院', u'建筑工程学院'),
            (u'材料科学与工程学院',u'材料科学与工程学院'),
            (u'理学院', u'理学院'),
            (u'文学与新闻传播学院', u'文学与新闻传播学院'),
            (u'法学院', u'法学院'),
            (u'美术学院', u'美术学院'),
            (u'体育学院', u'体育学院'),
            (u'鲁泰纺织服装学院', u'鲁泰纺织服装学院'),
            (u'交通与车辆工程学院', u'交通与车辆工程学院'),
            (u'电气与电子工程学院', u'电气与电子工程学院'),
            (u'化学工程学院', u'化学工程学院'),
            (u'资源与环境工程学院', u'资源与环境工程学院'),
            (u'生命科学学院', u'生命科学学院'),
            (u'商学院', u'商学院'),
            (u'外国语学院', u'外国语学院'),
            (u'马克思主义学院', u'马克思主义学院'),
            (u'音乐学院', u'音乐学院'),
            (u'国防教育学院', u'国防教育学院')], validators=[Required()]) 
    stumajor = StringField(u'专业', validators=[Required()])
    stuclass = StringField(u'班级', validators=[Required()])

class TeaForm(BaseForm):
    teaid1 = SelectField(u'教师工号1', choices=[('1','1'),('2','2')], validators=[Required()])
    teaid2 = SelectField(u'教师工号2', choices=[('2','2'),('1','1')], validators=[Required()])

class MainForm(BaseForm):
    comname = SelectField(u'竞赛项目', choices=[(u'国际大学生数学建模竞赛',u'国际大学生数学建模竞赛')], validators=[Required()])
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
    commain = FormField(MainForm,u'竞赛信息')
    comstu1 = FormField(StuForm, u'参赛学生1') 
    comstu2 = FormField(StuForm, u'参赛学生2') 
    comstu3 = FormField(StuForm, u'参赛学生3') 
    comstu4 = FormField(StuForm, u'参赛学生4') 
    comstu5 = FormField(StuForm, u'参赛学生5') 
    comtea = FormField(TeaForm, u'指导老师')
    submit = SubmitField(u'提交')

class PerForm(MainForm, StuForm, TeaForm):
    submit = SubmitField(u'提交')

