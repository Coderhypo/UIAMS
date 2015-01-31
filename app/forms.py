#-*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField, StringField, BooleanField, SelectField, FormField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, EqualTo, ValidationError
from flask.ext.login import current_user
from models import Acachemy, Teacher, ComName, User, Role

def Aca_all():
    Aca = []
    for a in Acachemy.query.all():
        Aca.append((str(a.id),a.aca_name))
    return Aca

def Tea_all():
    Tea_name = []
    for t in Teacher.query.all():
        tea = t.tea_id + ' ' + t.tea_name + ' ' + t.tea_unit
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

class AddUserForm(BaseForm):

    '''添加用户的表单类'''

    add_user_id = StringField(u'用户ID', validators=[Required()])
    add_user_name = StringField(u'用户名称', validators=[Required()])
    add_user_role = QuerySelectField(u'用户角色', get_label='role_name')
    add = SubmitField(u'添加')
    
    def validate_add_user_id(form, field):
        user = User.query.filter_by(user_id=field.data).first()
        if user != None:
            raise ValidationError(u'此用户ID已存在')

    def validate_add_user_name(form, field):
        user = User.query.filter_by(user_name=field.data).first()
        if user != None:
            raise ValidationError(u'此用户名称已存在')

class DelUserForm(BaseForm):

    '''删除用户的表单类'''

    del_user_name = QuerySelectField(u'选择用户', get_label='user_name')
    delete = SubmitField(u'删除')

    def validate_del_user_name(form, field):
        user = field.data
        if user == current_user:
            raise ValidationError(u'不能删除自己')

class ReSetUserForm(BaseForm):

    '''修改用户信息的表单类'''

    re_user_name = QuerySelectField(u'选择用户', get_label='user_name')
    re_user_role = QuerySelectField(u'修改角色', get_label='role_name')
    re_user_passwd = StringField(u'新密码') 
    reset = SubmitField(u'修改')

class AddTeaForm(BaseForm):
    add_tea_id = StringField(u'教师编号', validators=[Required()])
    add_tea_name = StringField(u'教师姓名', validators=[Required()])
    add_tea_unit = StringField(u'单位', validators=[Required()])
    add = SubmitField(u'添加')

class DelTeaForm(BaseForm):
    del_tea_id = QuerySelectField(u'选择教师', get_label='tea_name')
    delete = SubmitField(u'删除')

    def validate_del_tea_id(form, field):
        teacher_num = len(field.query)
        if teacher_num == 1:
            raise ValidationError(u'教师人数必须大于等于1')

class ReSetTeaForm(BaseForm):
    re_tea_id = QuerySelectField(u'选择教师', get_label='tea_name')
    re_tea_name = StringField(u'教师姓名', validators=[Required()])
    re_tea_unit = StringField(u'新单位')
    reset = SubmitField(u'修改')

class AddAcaForm(BaseForm):
    add_aca_id = StringField(u'学院编号', validators=[Required()])
    add_aca_name = StringField(u'学院编号', validators=[Required()])
    add = SubmitField(u'添加')

class DelAcaForm(BaseForm):
    del_aca_id = StringField(u'学院编号', validators=[Required()])
    del_aca_name = StringField(u'学院名称', validators=[Required()])
    delete = SubmitField(u'删除')

class ReSetAcaForm(BaseForm):
    re_teaid = StringField(u'学院编号', validators=[Required()])
    re_teaname = StringField(u'学院名称', validators=[Required()])
    re_passwd = StringField(u'新密码') 
    re = SubmitField(u'修改')
