import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import requests


default_start_year = 2020
default_start_month = 1
default_start_day = 1

def get_default_start_date():
    return dt.date(default_start_year, default_start_month, default_start_day)



def fetch_stock_data(stock_symbol: str, start:dt.date = get_default_start_date(), end:dt.date = dt.date.today()):
    yf.pdr_override()

    df = pdr.get_data_yahoo(stock_symbol, start, end)

    return df

def timestamp_to_date(stamp:str):
    dateArr = stamp.split(" ")[0].split("-")
    return dt.date(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]))



def get_company_name_for_symbol(stock_symbol:str):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(stock_symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == stock_symbol:
            return x['name']

