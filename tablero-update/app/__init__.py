import os

from flask import Flask
from flask_mail import Mail, Message
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from config import config

mongo = PyMongo()
mail = Mail()
moment = Moment()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)

    mongo.init_app(app)
    login_manager.init_app(app)
    
    bootstrap = Bootstrap(app)

    with app.app_context():
        from app.main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        from app.auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .plotlydash.dashboard import init_dashboard
        app = init_dashboard(app)

    return app