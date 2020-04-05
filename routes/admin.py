from flask import Blueprint, render_template, Flask, request
import random
import db
from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

bp = Blueprint('admin', __name__)


@bp.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        comp_data = db.Stock.query.filter_by(stock_symbol=ticker).first()
        main(ticker)
        return render_template('stocks.html', values=db.Smarket.query.all(), comp_data=comp_data)
    else:
        user = db.get_all_users()
        return render_template('admin.html', users=user)


def main(ticker):
    stock_symbol = ticker

    #clear existing data
    db.db.session.query(db.Smarket).delete()
    db.db.session.commit()

    # get the stock data
    stock_data = get_stock(stock_symbol)
    # populate the database
    populate_database(stock_symbol, stock_data, db)

def get_stock(stock_symbol):
    yf.pdr_override()

    start_year = 2020
    start_month = 1
    start_day = 1

    start = dt.datetime(start_year, start_month, start_day)
    now = dt.datetime.now()

    df = pdr.get_data_yahoo(stock_symbol, start, now)

    return df


def populate_database(stock_symbol, stock_data, db):
    df = stock_data

    for i in df.index:
        # insert the values into the database
        db.db.session.add(db.Smarket(stock_name=stock_symbol, date=str(i), open=str(df['Open'][i]), high=float(df['High']
                                                                  [i]), low=float(df['Low'][i]), close=float(df['Close'][i]), adj_close=float(df['Adj Close'][i]), volume=float(df['Volume'][i])))
        db.db.session.commit()        