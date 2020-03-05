import os
import requests
import click
from datetime import date, timedelta

from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

dba = SQLAlchemy()

from db.tables import *
from stock_fetcher import top100


def init_app(app):
    with app.app_context():
        dba.init_app(app)
        dba.create_all()
        app.cli.add_command(populate_db)


@click.command('populate-db')
@with_appcontext
def populate_db():
    populate_users()
    populate_stocks()
    populate_stock_history()


def populate_users():
    click.echo(f'Retrieving user data from Mockaroo...')

    url = 'https://my.api.mockaroo.com/users.json'
    params = {
        'key': os.environ['API_KEY_MOCKAROO']
    }

    response = requests.get(url, params=params)

    # only add users if successful response
    if response.status_code == 200:

        json_users = response.json()

        errors = 0

        with click.progressbar(json_users, label='Populating user table...') as progress_bar:
            for user in progress_bar:
                error = create_user(user)
                if error:
                    errors += 1

        # return a summary and print it to console
        click.echo(f'Finished with {errors} errors.')

    else:
        # display erroneous responses
        click.echo(response.json())


def populate_stocks():

    with click.progressbar(top100.tickers, label='Populating stock table...') as progress_bar:
        for symbol in progress_bar:
            stock = {
                'stock_symbol': symbol
            }
            add_stock(stock)


def populate_stock_history():
    url = 'https://api.worldtradingdata.com/api/v1/history'

    thirty_days_ago = str(date.today() - timedelta(days=30))

    with click.progressbar(top100.tickers, label='Populating stock history table...') as progress_bar:

        errors = 0
        unrecognized_symbols = []

        # begin iterating through stock symbols
        for stock_symbol in progress_bar:

            # create params
            params = {
                'symbol': stock_symbol,
                'api_token': os.environ['API_KEY_WORLDTRADINGDATA'],    # throws an error without this
                'date_from': thirty_days_ago    # get 30 days of stock data
            }

            # make the request
            response = requests.get(url, params=params)

            # add the stock data
            if response.status_code == 200:
                stock_data = response.json()

                # error if "Message" is in the response
                if 'Message' in stock_data:
                    errors += 1
                    unrecognized_symbols.append(stock_symbol)
                else:
                    # attempt to add the stock history
                    error = add_stock_history(stock_data)
                    if error:
                        errors += 1
            else:
                errors += 1

    # return a summary and print it to console
    click.echo(f'Finished with {errors} errors.')
    click.echo(f'Symbols not found: {unrecognized_symbols}')


# Queries


def create_user(user):
    """
    Verifies input and returns any errors.  If there aren't any errors,
    create the user.

    :param user: the user in JSON format
    :return: None if added successfully, otherwise the error
    """

    if 'email' not in user:
        return 'Email required'

    existing_user = bool(User.query.filter(User.email == user['email']).first())

    if existing_user:
        return 'This email address is already registered'
    elif 'password' not in user:
        return 'Password required'
    elif 'first-name' not in user:
        return 'First name required'
    elif 'last-name' not in user:
        return 'Last name required'

    new_user = User(
        email=user['email'],
        password=generate_password_hash(user['password']),
        first_name=user['first-name'],
        last_name=user['last-name'],

        # null values permitted
        address=user.get('address', None),
        city=user.get('city', None),
        state=user.get('state', None),
        zip_code=user.get('zip-code', None),
        telephone=user.get('telephone', None)
    )

    dba.session.add(new_user)
    dba.session.commit()


def add_stock(stock):
    """
    Adds a stock to the Stock table

    :return: None if added successfully, otherwise the error
    """

    if 'stock_symbol' not in stock:
        return 'stock_symbol required'

    new_stock = Stock(
        stock_symbol=stock['stock_symbol'],
        company_name=stock.get('company_name', None)
    )

    dba.session.add(new_stock)
    dba.session.commit()


def add_stock_history(stock_data):
    """
    Adds the given stock data to the stock history table.  Stock_data should be formatted as shown below.

    stock_data = {
        "name": <Stock Symbol>,
        "history": {
            "2020-03-03": {
                "open": <Float>,
                "close": <Float>,
                "high": <Float>,
                "low": <Float>,
                "volume": <Integer>,
            },
            ...
        }
    }

    :param stock_data: the stock data
    :return: None if added successfully, otherwise the error
    """

    symbol = stock_data['name']
    stock = Stock.query.filter(Stock.stock_symbol == symbol).first()

    if stock is None:
        return f'No stock in database matching {symbol}.'

    history = stock_data['history']

    for date_str, trade_data in history.items():
        new_stock_history = Stock_History(
            date=date.fromisoformat(date_str),
            fk_stock_id=stock.id,
            high=trade_data['high'],
            low=trade_data['low'],
            open=trade_data['open'],
            close=trade_data['close'],
            volume=trade_data['volume']
        )

        dba.session.add(new_stock_history)
        dba.session.commit()


def get_stock_history_by_symbol(symbol):
    """

    :param symbol: the symbol to lookup
    :return: the history of the stock matching the symbol or None
    """
    stock = Stock.query.filter(Stock.stock_symbol == symbol).first()

    if stock is None:
        return None

    return Stock_History.query.filter(Stock_History.fk_stock_id == stock.id).all()
