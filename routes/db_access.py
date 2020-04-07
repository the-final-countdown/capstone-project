import functools

from flask import Blueprint, request, render_template, session, g, redirect, url_for, flash
from werkzeug.security import check_password_hash

import db

import json

bp = Blueprint('db_access', __name__)


@bp.route('/get_user_transactions_ajax', methods=('GET', 'POST'))
def get_user_transactions():
    # print(g.user)

    retVal = {'error': 'none'}

    if g.user is None:
        retVal['error'] = "No user is logged in."
        return json.dumps(retVal)

    return json.dumps(g.user.get_portfolios())



@bp.route('/get_user_portfolios', methods=('GET', 'POST'))
def get_user_transactions():
    # print(g.user)

    retVal = {'error': 'none'}

    if g.user is None:
        retVal['error'] = "No user is logged in."
        return json.dumps(retVal)



    return render_template('stocks.html', values=g.user.get_portfolios())




@bp.route('/get_user_portfolios/<int:user_id>', methods=('GET', 'POST'))
def get_specific_user_transactions(user_id: int):

    retVal = {'error': 'none'}

    if g.user is None:
        retVal['error'] = "not logged in"
        return json.dumps(retVal)


    if not g.user.is_admin:
        retVal['error'] = "logged in user must be admin"
        return json.dumps(retVal)

    accessed_user = db.get_user_by_id(user_id)

    if accessed_user is None:
        if not g.user.is_admin:
            retVal['error'] = "user does not exist"
            return json.dumps(retVal)


    for pf in g.user.get_portfolios():
        add_tr = {}

        for tr in pf.get_transactions():
            add_tr[str(tr.purchase_date)] = tr.ToDict()

        retVal[pf.display_name] = add_tr

    return json.dumps(retVal)




