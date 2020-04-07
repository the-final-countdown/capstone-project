import functools

from flask import Blueprint, request, render_template, session, g, redirect, url_for, flash
from werkzeug.security import check_password_hash

import db

import json

bp = Blueprint('db_access', __name__)


@bp.route('/user_portfolios_ajax', methods=('GET', 'POST'))
def user_portfolios_ajax():
    # print(g.user)

    retVal = {'error': 'none'}

    if g.user is None:
        retVal['error'] = "No user is logged in."
        return json.dumps(retVal)

    return json.dumps(g.user.get_portfolios())



@bp.route('/user_portfolios', methods=('GET', 'POST'))
def user_portfolios():
    # print(g.user)

    return specific_user_portfolios(g.user.id)


@bp.route('/user_portfolios/<int:user_id>', methods=('GET', 'POST'))
def specific_user_portfolios(user_id: int):

    retVal = {'error': 'none'}

    if g.user is None:
        retVal['error'] = "not logged in"
        return json.dumps(retVal)


    if (not g.user.is_admin) and g.user.id != user_id:
        retVal['error'] = "logged in user must be admin or owner of account"
        return json.dumps(retVal)


    accessed_user: db.User = db.get_user_by_id(user_id)

    if accessed_user is None:
        retVal['error'] = "user does not exist"
        return json.dumps(retVal)

    return render_template('portfolio.html', values={
        "user": accessed_user,
        "portfolios": accessed_user.get_portfolios(),
     })


@bp.route('/user_portfolios/<int:user_id>/<int:portfolio_id>', methods=('GET', 'POST'))
def portfolio_transactions(user_id: int, portfolio_id: int):
    retVal = {'error': 'none'}


    if g.user is None:
        retVal['error'] = "not logged in"
        return json.dumps(retVal)


    accessed_user: db.User = db.get_user_by_id(user_id)
    if accessed_user is None:
        retVal['error'] = "user does not exist"
        return json.dumps(retVal)

    if (not g.user.is_admin) and g.user.id != user_id:
        retVal['error'] = "logged in user must be admin or owner of portfolio"
        return json.dumps(retVal)

    accessed_portfolio: db.Portfolio = accessed_user.get_portfolio_by_id(portfolio_id)
    if accessed_portfolio is None:
        retVal['error'] = "portfolio does not exist"
        return json.dumps(retVal)

    print(accessed_portfolio.display_name)

    print(accessed_portfolio.get_transactions())

    return render_template('transactions.html', values={
        "user": accessed_user,
        "portfolio": accessed_portfolio,
        "transactions": accessed_portfolio.get_transactions()
    })



