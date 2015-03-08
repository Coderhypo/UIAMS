from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from competition import competition as competition_blueprint
    app.register_blueprint(competition_blueprint, url_prefix='/competition')

    from thesis import thesis as thesis_blueprint
    app.register_blueprint(thesis_blueprint, url_prefix='/thesis')
    
    from patent import patent as patent_blueprint
    app.register_blueprint(patent_blueprint, url_prefix='/patent')

    login_manager.setup_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login'

    return app

