from flask.ext.script import Manager, Server
from app import app,db

manager = Manager(app)

manager.add_command("start", Server(host="0.0.0.0", port=5000, use_debugger=True))
@manager.command
def initdb():
    db.create_all()
@manager.command
def dropdb():
    db.drop_all()

if __name__ == '__main__':
    manager.run()
