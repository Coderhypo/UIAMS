#-*- coding: UTF-8 -*-
import os
from app import app, db
from app.models import User, Role
from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
def make_shell_context():
    return dict(app=app, db=db,  User=User, Role=Role)

manager.add_command("runserver", Server(host="0.0.0.0", port=2000))
manager.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    from flask.ext.migrate import upgrade
    from app.models import Role

    # migrate database to latest revision
    upgrade()

    Role.insert_roles()
    admin_role = Role.query.filter_by(role_name='管理员').first()

    '''
    admin = User('admin', 'admin')
    admin.password = '123'
    admin.role = admin_role

    db.session.add(admin)
    db.session.commit()
    '''

if __name__ == '__main__':
    manager.run()
