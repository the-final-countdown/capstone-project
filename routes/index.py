from flask import Blueprint, render_template

import db

bp = Blueprint('portfolio', __name__)


@bp.route('/')
def index():
    stocks = db.get_all_stocks()
    return render_template('index.html', stocks=stocks)