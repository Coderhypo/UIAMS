#-*- coding: UTF-8 -*-
from app import app,db
from app.models import ComName, User, Acachemy, Role, Teacher
from flask.ext.script import Manager, Server, Shell
from app import views

manager = Manager(app)
def make_shell_context():
    return dict(app=app, db=db, Acachemy=Acachemy,  User=User, Role=Role, createdb=createdb)

manager.add_command("start", Server(host="0.0.0.0", port=5000, use_debugger=True))
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
