import os

from flask import Flask

import db

# route blueprints
from routes import index
from routes import auth
from routes import admin


def create_app(test_config=None):

    # create the app and load config variables
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///capstone-project.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # initialize the db
    db.init_app(app)

    # ROUTES

    # main page
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    # login and registration
    app.register_blueprint(auth.bp)

    # admin
    app.register_blueprint(admin.bp)

    return app
