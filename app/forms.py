from flask.ext.wtf import Form
from wtforms import PasswordField, SubmitField, StringField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
    
class MainForm(Form):
    pass
