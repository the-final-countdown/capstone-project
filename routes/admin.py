from flask import Blueprint, render_template

from db.tables import User, Portfolio

bp = Blueprint('admin', __name__)


@bp.route('/admin')
def admin():
    users = User.query.all()

    return render_template('admin.html', users=users)
