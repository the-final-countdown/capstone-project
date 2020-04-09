from flask import Blueprint, flash, render_template

import routes.db_access

bp = Blueprint('portfolio', __name__)

@bp.route('/')
def index():
    return render_template('index.html')
    # return routes.db_access.user_portfolios()