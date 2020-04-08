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
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'postgres://rwnmikduijwbqd:a19f5a7ac5889d6af1c7342bbc25f26a5d2f14580d588d511911c3b8b26b0cc6@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d85e2kc82esup2'), 
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
