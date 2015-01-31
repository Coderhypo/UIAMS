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
   
class StudentForm(BaseForm):
    
    '''学生信息的表单类'''

    student_id = StringField(u'学号', validators=[Required()])
    student_name = StringField(u'姓名', validators=[Required()])
    acachemys = QuerySelectField(u'学院', get_label='aca_name')
    student_major = StringField(u'专业', validators=[Required()])
    student_class = StringField(u'班级', validators=[Required()])

class TeacherForm(BaseForm):
    
    '''教师的表单类'''

    teachers1 = QuerySelectField(u'指导教师1', get_label='tea_name')
    teachers2 = QuerySelectField(u'指导教师2', get_label='tea_name')

# 竞赛表单类

class CompetitionInfoForm(BaseForm):

    '''竞赛信息的表单类'''

    competitions_name = QuerySelectField(u'竞赛项目', get_label='com_name')
    project_name = StringField(u'成果名称')
    competition_level = SelectField(u'获奖级别', choices=[
            (u'省级',u'省级'), 
            (u'国家级',u'国家级'), 
            (u'亚洲区级',u'亚洲区级'), 
            (u'国际',u'国际')], validators=[Required()])
    competition_class = SelectField(u'等级', choices=[
            (u'一等奖（金奖）',u'一等奖（金奖）'), 
            (u'二等奖（银奖）',u'二等奖（银奖）'), 
            (u'三等奖（铜奖）',u'三等奖（铜奖）')], validators=[Required()])
    competition_date = StringField(u'获奖时间', validators=[Required()])
    competition_org = StringField(u'颁奖单位', validators=[Required()])

    def validate_competition_data(form, field):
        print field.data
        if field.data == '':
            raise ValidationError(u'请填写此字段')

class CompetitionIndividualForm(TeacherForm, CompetitionInfoForm, StudentForm):
    
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

class CreateUserForm(BaseForm):

    '''添加用户的表单类'''

    create_id = StringField(u'用户ID', validators=[Required()])
    create_name = StringField(u'用户名称', validators=[Required()])
    roles = QuerySelectField(u'用户角色', get_label='role_name')
    create = SubmitField(u'添加')
    
    def validate_create_id(form, field):
        user = User.query.filter_by(user_id=field.data).first()
        
        if user != None:
            raise ValidationError(u'此用户ID已存在')

    def validate_create_name(form, field):
        user = User.query.filter_by(user_name=field.data).first()
        
        if user != None:
            raise ValidationError(u'此用户名称已存在')

class DeleteUserForm(BaseForm):

    '''删除用户的表单类'''

    users = QuerySelectField(u'选择用户', get_label='user_name')
    delete = SubmitField(u'删除')

    def validate_users(form, field):
        user = field.data
        
        if user == current_user:
            raise ValidationError(u'不能删除自己')

class UpdateUserForm(BaseForm):

    '''修改用户信息的表单类'''

    users = QuerySelectField(u'选择用户', get_label='user_name')
    roles = QuerySelectField(u'修改角色', get_label='role_name')
    update_name = StringField(u'用户名称')
    update_passwd = StringField(u'密码') 
    update = SubmitField(u'修改')

    def validate_update_name(form, field):
        user = User.query.filter_by(user_name=field.data).first()
        
        if user != None:
            raise ValidationError(u'该用户名称已存在')


# 教师表单类

class CreateTeacherForm(BaseForm):

    '''添加教师的表单类'''

    create_id = StringField(u'教师编号', validators=[Required()])
    create_name = StringField(u'教师姓名', validators=[Required()])
    create_unit = StringField(u'单位', validators=[Required()])
    create = SubmitField(u'添加')

    def validate_create_id(form, field):
        teacher = Teacher.query.filter_by(tea_id=field.data).first()

        if teacher != None:
            raise ValidationError(u'此教师编号已存在')

    def validate_create_name(form, field):
        teacher = Teacher.query.filter_by(tea_name=field.data).first()

        if teacher != None:
            raise ValidationError(u'该教师姓名已存在')

class DeleteTeacherForm(BaseForm):

    '''删除教师的表单类'''

    teachers = QuerySelectField(u'选择教师', get_label='tea_name')
    delete = SubmitField(u'删除')

    def validate_teachers(form, field):
        teacher_number = len(field.query)

        if teacher_number == 1:
            raise ValidationError(u'教师不能为空')

class UpdateTeacherForm(BaseForm):
    
    '''更新教师信息的表单类'''

    teachers = QuerySelectField(u'选择教师', get_label='tea_name')
    update_name = StringField(u'教师姓名')
    update_unit = StringField(u'新单位')
    update = SubmitField(u'修改')

    def validate_update_name(form, field):
        teacher = Teacher.query.filter_by(tea_name=field.data).first()
        if teacher != None:
            raise ValidationError(u'该教师姓名已存在')

# 学院表单类

class CreateAcachemyForm(BaseForm):

    '''添加学院的表单类'''

    create_name = StringField(u'学院名称', validators=[Required()])
    create = SubmitField(u'添加')

    def validate_create_name(form, field):
        acachemy = Acachemy.query.filter_by(aca_name=field.data).first()
        if acachemy != None:
            raise ValidationError(u'该学院已存在')

class DeleteAcachemyForm(BaseForm):
    
    '''删除学院的表单类'''

    acachemys = QuerySelectField(u'选择学院', get_label='aca_name')
    delete = SubmitField(u'删除')
    
    def validate_acachemys(form, field):
        acachemy_number = len(field.query)

        if acachemy_number == 1:
            raise ValidationError(u'学院不能为空')

class UpdateAcachemyForm(BaseForm):
    
    '''修改学院信息的表单类'''  

    acachemys = QuerySelectField(u'选择学院', get_label='aca_name')
    update_name = StringField(u'学院名称', validators=[Required()])
    update = SubmitField(u'修改')

    def validate_update_name(form, field):
        acachemy = Acachemy.query.filter_by(aca_name=field.data).first()
        if acachemy != None:
            raise ValidationError(u'该学院已存在')
