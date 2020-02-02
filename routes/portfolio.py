from flask import Blueprint, render_template

bp = Blueprint('portfolio', __name__)


@bp.route('/')
def index():
    return render_template('portfolio.html')