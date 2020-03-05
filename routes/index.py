from flask import Blueprint, render_template

from db.tables import Stock

bp = Blueprint('portfolio', __name__)


@bp.route('/')
def index():
    stocks = Stock.query.all()
    return render_template('index.html', stocks=stocks)