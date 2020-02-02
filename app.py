import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'capstone-project.sqlite')
    )

    if test_config is None:
        # load the instance config when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config
        app.config.from_mapping(test_config)

    # create the instance folder, if necessary
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    import db
    db.init_app(app)

    # route for main page
    from routes import portfolio
    app.register_blueprint(portfolio.bp)
    app.add_url_rule('/', endpoint='index')

    # routes to login and register
    from routes import auth
    app.register_blueprint(auth.bp)

    # route to admin page
    from routes import admin
    app.register_blueprint(admin.bp)

    # return the newly created app
    return app
