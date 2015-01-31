#-*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField, StringField, BooleanField, SelectField, FormField, DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, ValidationError
from flask.ext.login import current_user
from models import Acachemy, Teacher, User,Patent

class BaseForm(Form):

    '''支持中文表单的表单基类'''

    LANGUAGES = ['zh']

class LoginForm(BaseForm):

    '''登录的表单类'''

    userid = StringField(u'帐号', validators=[Required()])
    passwd = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登入')
   
class StuForm(BaseForm):
    
    '''学生信息的表单类'''

    stu_id = StringField(u'学号', validators=[Required()])
    stu_name = StringField(u'姓名', validators=[Required()])
    stu_acachemy = QuerySelectField(u'学院', get_label='aca_name')
    stu_major = StringField(u'专业', validators=[Required()])
    stu_class = StringField(u'班级', validators=[Required()])

class TeaForm(BaseForm):
    
    '''教师的表单类'''

    tea1 = QuerySelectField(u'指导教师1', get_label='tea_name')
    tea2 = QuerySelectField(u'指导教师2', get_label='tea_name')

# 竞赛表单类

class ComInfoForm(BaseForm):

    '''竞赛信息的表单类'''

    com_name = QuerySelectField(u'竞赛项目', get_label='com_name')
    pro_name = StringField(u'成果名称')
    com_level = SelectField(u'获奖级别', choices=[
            (u'省级',u'省级'), 
            (u'国家级',u'国家级'), 
            (u'亚洲区级',u'亚洲区级'), 
            (u'国际',u'国际')], validators=[Required()])
    com_class = SelectField(u'等级', choices=[
            (u'一等奖（金奖）',u'一等奖（金奖）'), 
            (u'二等奖（银奖）',u'二等奖（银奖）'), 
            (u'三等奖（铜奖）',u'三等奖（铜奖）')], validators=[Required()])
    com_date = DateField(u'获奖时间', validators=[Required()])
    com_org = StringField(u'颁奖单位', validators=[Required()])

class ComIndivForm(TeaForm, ComInfoForm, StuForm):
    
    '''个人竞赛的表单类'''

    submit = SubmitField(u'提交')

class ComTeamForm():
    
    '''团体竞赛的表单类'''

    pass

class PatentForm(BaseForm):

    '''专利信息的表单类'''

    type = SelectField(u'专利类型',choices=[
        (u'学术专著',u'学术专著'),
        (u'科普读物',u'科普读物'),
        (u'电子出版物',u'电子出版物')],validators=[Required()])
    peaname = StringField(u'专利名称:',validators=[Required()])
    inventor = StringField(u'发明人:')
    filingdate = StringField(u'专利申请日')
    patentee = StringField(u'专利权人')
    announcement = StringField(u'授权公告日')
    submit = SubmitField(u'提交')

    def validate_add_patent (form,field):
        Pat_info = Patent.query.filter_by(pea_name = field.data).first()
        if Pat_info != None:
            raise ValidationError(u'专利名称已存在')
    

# 用户表单类

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

    del_user = QuerySelectField(u'选择用户', get_label='user_name')
    delete = SubmitField(u'删除')

    def validate_del_user(form, field):
        user = field.data
        if user == current_user:
            raise ValidationError(u'不能删除自己')

class ReSetUserForm(BaseForm):

    '''修改用户信息的表单类'''

    re_user = QuerySelectField(u'选择用户', get_label='user_name')
    re_user_role = QuerySelectField(u'修改角色', get_label='role_name')
    re_user_passwd = StringField(u'新密码') 
    reset = SubmitField(u'修改')

# 教师表单类

class AddTeaForm(BaseForm):

    '''添加教师的表单类'''

    add_tea_id = StringField(u'教师编号', validators=[Required()])
    add_tea_name = StringField(u'教师姓名', validators=[Required()])
    add_tea_unit = StringField(u'单位', validators=[Required()])
    add = SubmitField(u'添加')

    def validate_add_tea_id(form, field):
        teacher = Teacher.query.filter_by(tea_id=field.data).first()
        if teacher != None:
            raise ValidationError(u'此教师编号已存在')

    def validate_add_tea_name(form, field):
        teacher = Teacher.query.filter_by(tea_name=field.data).first()
        if teacher != None:
            raise ValidationError(u'此教师姓名已存在')

class DelTeaForm(BaseForm):

    '''删除教师的表单类'''

    del_tea = QuerySelectField(u'选择教师', get_label='tea_name')
    delete = SubmitField(u'删除')

    def validate_del_tea(form, field):
        teacher_num = len(field.query)
        if teacher_num == 1:
            raise ValidationError(u'教师人数必须大于等于1')

class ReSetTeaForm(BaseForm):
    
    '''修改教师信息的表单类'''

    re_tea = QuerySelectField(u'选择教师', get_label='tea_name')
    re_tea_name = StringField(u'教师姓名')
    re_tea_unit = StringField(u'新单位')
    reset = SubmitField(u'修改')

# 学院表单类

class AddAcaForm(BaseForm):

    '''添加学院的表单类'''

    add_aca_name = StringField(u'学院名称', validators=[Required()])
    add = SubmitField(u'添加')

    def validate_add_aca_name(form, field):
        acachemy = Acachemy.query.filter_by(aca_name=field.data).first()
        if acachemy != None:
            raise ValidationError(u'该学院已存在')

class DelAcaForm(BaseForm):
    
    '''删除学院的表单类'''

    del_aca = QuerySelectField(u'选择学院', get_label='aca_name')
    delete = SubmitField(u'删除')

class ReSetAcaForm(BaseForm):
    
    '''修改学院信息的表单类'''  

    re_aca = QuerySelectField(u'选择学院', get_label='aca_name')
    re_aca_name = StringField(u'学院名称', validators=[Required()])
    reset = SubmitField(u'修改')
