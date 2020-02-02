from flask import Blueprint, render_template, url_for

bp = Blueprint('admin', __name__)


@bp.route('/admin')
def admin():
    return render_template('admin.html')