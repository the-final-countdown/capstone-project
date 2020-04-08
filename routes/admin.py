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


    user = db.get_all_users()
    return render_template('admin.html', users=user)

    # if request.method == 'POST':
    #     user_id = request.form.get('user-id')
    #     data = db.Portfolio.query.filter_by(user_id=user_id).all()
    #     return render_template('portfolio.html', values=data)
    # else:
    #     user = db.get_all_users()
    #     return render_template('admin.html', users=user)

@bp.route('/admin/db_control', methods=['GET', 'POST'])
def db_control_page():
    retVal = {'error': 'none'}

    if g.user is None:
        retVal['error'] = "not logged in"
        return json.dumps(retVal)

    if not g.user.is_admin:
        retVal['error'] = "logged in user must be admin"
        return json.dumps(retVal)


    user = db.get_all_users()
    return render_template('db_control.html')


@bp.route('/admin/db_control/command', methods=['GET', 'POST'])
def populate_database():
    # capture_sdout: bool = (request.form.get('capture_sdout') != 'FALSE')
    capture_sdout: bool = (request.form.get('capture_sdout').upper() == 'TRUE')

    old_sdout = sys.stdout

    if capture_sdout:


        sys.stdout = StringIO()

    out = {
        'success': True,
        'output': ""
    }

    try:

        retVal = {'error': 'none'}

        if g.user is None:
            retVal['error'] = "not logged in"
            return json.dumps(retVal)

        if not g.user.is_admin:
            retVal['error'] = "logged in user must be admin"
            return json.dumps(retVal)

        cmd = request.form.get('cmd')

        # if request.method == 'POST':

        print(f"population has started: {cmd}" )



        if cmd == 'clear_db':
            db.clear_db(g.user)

        elif cmd == 'populate_users':
            db.populate_users()


        elif cmd == 'populate_stocks':
            db.populate_stocks()

        elif cmd == 'clean_stocks':
            db.clean_stocks()

        elif cmd == 'populate_stock_history':
            db.populate_stock_history()

        elif cmd == 'generate_portfolios':
            db.generate_portfolios()

        else:
            message = f"{cmd} is not a valid command"

            out['success'] = False
            out['output'] = message

            print(message)

        # ####
         # capture output


        if capture_sdout:
            if out['success']:
                out['output'] = sys.stdout.getvalue()  # release output

            sys.stdout.close()  # close the stream
            sys.stdout = old_sdout  # restore original stdout

            print(out)

        return json.dumps(out)  # post processing

    except Exception as e:


        if capture_sdout:
            out['output'] = sys.stdout.getvalue() + "\n<hr/>ERROR:" + str(e) # release output
            # ####

            sys.stdout.close()  # close the stream
            sys.stdout = old_sdout  # restore original stdout

            print(out)

        return json.dumps(out)  # post processing




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