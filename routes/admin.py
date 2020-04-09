from flask import Blueprint, render_template, Flask, request, g
import random
import db
from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import json

import sys
from flask_sqlalchemy import SQLAlchemy
from io import StringIO

import subprocess

bp = Blueprint('admin', __name__)


@bp.route('/admin', methods=['GET', 'POST'])
def admin():

    retVal = {'error': 'none'}

    if g.user is None:
        retVal['error'] = "not logged in"
        return json.dumps(retVal)

    if not g.user.is_admin:
        retVal['error'] = "logged in user must be admin"
        return json.dumps(retVal)


    users = db.get_all_users()
    return render_template('admin.html', users=users)

    # if request.method == 'POST':
    #     user_id = request.form.get('user-id')
    #     data = db.Portfolio.query.filter_by(user_id=user_id).all()
    #     return render_template('portfolio.html', values=data)
    # else:
    #     user = db.get_all_users()
    #     return render_template('admin.html', users=user)


@bp.route('/admin/user_search', methods=['GET', 'POST'])
def user_search():
    retVal = {'error': 'none'}

    if g.user is None:
        retVal['error'] = "not logged in"
        return json.dumps(retVal)

    if not g.user.is_admin:
        retVal['error'] = "logged in user must be admin"
        return json.dumps(retVal)


    user_id = request.form.get('uid')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    email = request.form.get('email')

    if user_id is None:
        user_id = ""

    if first_name is None:
        first_name = ""

    if last_name is None:
        last_name = ""

    if email is None:
        email = ""


    users = db.User.query.filter(db.dba.and_(db.User.id.match(f"%{user_id}%"),
                                             db.User.first_name.match(f"%{first_name}%"),
                                             db.User.last_name.match(f"%{last_name}%"),
                                             db.User.email.match(f"%{email}%")))
    return render_template('user_search.html', users=users)




@bp.route('/js/admin-db-control.js', methods=['GET', 'POST'])
def get_populate_database_js():
    return render_template('js/admin-db-control.js')




# def main(ticker):
#     stock_symbol = ticker
#
#     #clear existing data
#     db.db.session.query(db.Smarket).delete()
#     db.db.session.commit()
#
#     # get the stock data
#     stock_data = get_stock(stock_symbol)
#     # populate the database
#     populate_database(stock_symbol, stock_data, db)
#
# def get_stock(stock_symbol):
#     yf.pdr_override()
#
#     start_year = 2020
#     start_month = 1
#     start_day = 1
#
#     start = dt.datetime(start_year, start_month, start_day)
#     now = dt.datetime.now()
#
#     df = pdr.get_data_yahoo(stock_symbol, start, now)
#
#     return df