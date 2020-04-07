import functools

from flask import Blueprint, request, render_template, session, g, redirect, url_for, flash
from werkzeug.security import check_password_hash

import db

import json

bp = Blueprint('db_access', __name__)

@bp.route('/get_user_transactions', methods=('GET', 'POST'))
def get_user_transactions():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
        return json.dumps({})
    else:
        g.user = db.get_user_by_id(user_id)

    print(g.user)

    retVal = {}

    for pf in g.user.get_portfolios():
        add_tr = {}

        for tr in pf.get_transactions():
            add_tr[str(tr.purchase_date)] = tr.ToDict()

        retVal[pf.display_name] = add_tr

    return json.dumps(retVal)

