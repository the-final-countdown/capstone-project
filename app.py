import os

from flask import Flask

import db

# route blueprints
from routes import portfolio
from routes import auth
from routes import admin


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY = 'dev',
    DATABASE = os.path.join(app.instance_path, 'capstone-project.sqlite')
)

# create the instance folder, if necessary
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# initialize the db
db.init_app(app)

# ~~~~~~ ROUTES ~~~~~~~

# main page
app.register_blueprint(portfolio.bp)
app.add_url_rule('/', endpoint='index')

# login and registration
app.register_blueprint(auth.bp)

# admin
app.register_blueprint(admin.bp)
