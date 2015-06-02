#_*_ coding: UTF-8 _*_
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babelex import Babel
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

    from admin_old import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin_old')

    from .admin import admin
    admin.init_app(app)

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return 'zh_hans_CN'

    login_manager.setup_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login'

from views import *
