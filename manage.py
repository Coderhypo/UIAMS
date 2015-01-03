from flask.ext.script import Manager, Server, Shell
from app.models import ComUser
from app import app,db

manager = Manager(app)
def make_shell_context():
    return dict(app=app, db=db, ComUser=ComUser)

manager.add_command("start", Server(host="0.0.0.0", port=5000, use_debugger=True))
manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def initdb():
    db.create_all()
@manager.command
def dropdb():
    db.drop_all()

if __name__ == '__main__':
    manager.run()
