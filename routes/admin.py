from flask import Blueprint, render_template

import db

bp = Blueprint('admin', __name__)


@bp.route('/admin')
def admin():
    user = db.get_all_users()

    return render_template('admin.html', users=user)