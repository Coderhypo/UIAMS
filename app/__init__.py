#_*_ coding= UTF-8 _*_
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from config import config
import os

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()

with app.app_context():
    config_name = os.getenv('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.app = app
    db.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from competition import competition as competition_blueprint
    app.register_blueprint(competition_blueprint, url_prefix='/competition')

    login_manager.setup_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login'
