from flask import Blueprint, render_template, Flask, request

import db

bp = Blueprint('admin', __name__)


@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        render_template('stocks.html')
    else:
        user = db.get_all_users()
        return render_template('admin.html', users=user)