import yfinance as yf

from . import top100


def get_top100():
    return top100.tickers


def get_stock_history(tickers, interval='1mo'):
    """
    :param tickers: a space separated string or a list of tickers
    :param interval: valid periods--1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    :return: a dict in the following format--
            {
                MSFT: {
                    '2020-03-04': {
                        open: 168.49,
                        close: 159.03,
                        high: 169.12,
                        low: 159.03,
                        volume: 981987
                    },
                    ...
                },
                AAPL: {
                    ...
                },
            }
    """

    if not tickers:
        return {}

    data = yf.download(
        tickers=tickers,
        period='ytd',
        interval=interval,
        group_by='ticker',
        threads=True,
        auto_adjust=True
    )

    return None  # but the data, eventually
