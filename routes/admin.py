from flask import Blueprint, render_template

from database import queries

bp = Blueprint('admin', __name__)


@bp.route('/admin')
def admin():
    user = queries.get_all_users()

    return render_template('admin.html', users=user)