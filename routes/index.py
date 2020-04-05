from flask import Blueprint, flash, render_template

bp = Blueprint('portfolio', __name__)

@bp.route('/')
def index():
    return render_template('index.html')