from flask.ext.script import Manager, Server, Shell
from app.models import ComName, ComUser, ComAca, ComRole, ComTea
from app import app,db
from app.forms import LoginForm

manager = Manager(app)
def make_shell_context():
    return dict(app=app, db=db, ComAca=ComAca,  ComUser=ComUser, ComRole=ComRole)

manager.add_command("start", Server(host="0.0.0.0", port=5000, use_debugger=True))
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def createdb():
    db.create_all()

@manager.command
def initdb():
    ComRole.insert_roles()
    ComAca.insert_acas()
    ComName.insert_cname()
    ComTea.insert_teas()
    admin_role = ComRole.query.filter_by(name='Administrator').first()
    admin = ComUser(user_name='admin', role_id=admin_role.id)
    admin.password='123'
    teacher_role = ComRole.query.filter_by(name='Teacher').first()
    teacher = ComUser(user_name='nplus', role_id=teacher_role.id)
    teacher.password='123'
    academy_role = ComRole.query.filter_by(name='Academy').first()
    academy = ComUser(user_name='aca', role_id=academy_role.id)
    academy.password='123'
    db.session.add_all([admin, teacher, academy])
    db.session.commit()

@manager.command
def dropdb():
    db.drop_all()

if __name__ == '__main__':
    manager.run()
