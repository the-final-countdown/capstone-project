import os
import requests
import click
# from datetime import datetime

from flask import jsonify
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

dba = SQLAlchemy()

from db.tables import *
from db import stock_handler as sth


def init_app(app):
    with app.app_context():
        dba.init_app(app)
        dba.create_all()

        # Adding click commands:
        app.cli.add_command(populate_users)
        app.cli.add_command(populate_stocks)
        app.cli.add_command(populate_stock_history)


@click.command('populate-users')
@with_appcontext
def populate_users():
    _process_mockaroo_query("https://my.api.mockaroo.com/users.json", create_user, "users")

    # url = f"https://my.api.mockaroo.com/users.json?key={os.environ.get('API_KEY_MOCKAROO')}"
    #
    # response = requests.get(url)
    #
    # # only add users if successful response
    # if response.status_code == 200:
    #
    #     json_users = response.json()
    #
    #     errors = 0
    #
    #     for user in json_users:
    #         error = create_user(user)
    #         if error is not None:
    #             errors += 1
    #
    #     users_added = len(json_users) - errors
    #
    #     # return a summary and print it to console
    #     click.echo(f'Added {users_added} users ({errors} errors)')
    #     return
    #
    # # display erroneous responses
    # click.echo(response.json())


@click.command('populate-stocks')
@with_appcontext
def populate_stocks():
    _process_mockaroo_query("https://my.api.mockaroo.com/stock_symbols.json", create_stock, "stocks")

@click.command('populate-stock-data')
@with_appcontext
def populate_stock_history():
    for stock in dba.engine.execute("SELECT * FROM STOCK").fetchall():
        rId = stock[0]
        rSymbol = stock[1]
        rName = stock[2]

        history = sth.fetch_stock_data(rSymbol)

        # if history.

        if len(history.index) <= 0:
            click.echo(rSymbol + " not found. Skipping... ")
            continue

        click.echo("generating for " + rSymbol + "... ")
        for i in history.index:

            new_history_dict = {
                "stock_id": rId,
                "date": sth.timestamp_to_date(str(i)),
                "high": history['High'][i],
                "low": history['Low'][i],
                "open": history['Open'][i],
                "close": history['Close'][i]
            }

            create_stock_history(new_history_dict)



    # dba.session.commit()



# Models



# Queries


def create_user(user):
    """
    Verifies input and returns any errors.  If there aren't any errors,
    create the user.

    :param user: the user in JSON format
    :return: An error message (if applicable) or None
    """

    if 'email' not in user:
        return 'Email required'
    elif get_user_by_email(user['email']) is not None:
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


def get_user_by_id(user_id):
    """
    Get the user by their id

    :param user_id: the id of the user
    :return: the user or None
    """
    return User.query.filter(User.id == user_id).first()


def get_user_by_email(email):
    """
    Get the user by their id

    :param email: the email address of the user
    :return: the user or None
    """
    return User.query.filter(User.email == email).first()


def get_all_users():
    """
    Returns all users
    """
    return User.query.order_by(User.last_name, User.first_name).all()




def create_stock(stock):

    if 'stock_symbol' not in stock:
        return 'Stock symbol required'

    stock_name = ""
    if 'stock_name' not in stock:
        stock_name = sth.get_company_name_for_symbol(stock['stock_symbol'])
    else:
        stock_name = stock['stock_name']

    new_stock = Stock(stock_symbol=stock['stock_symbol'], company_name=stock_name)

    dba.session.add(new_stock)
    dba.session.commit()

def create_stock_history(stock_history):

    # if 'stock_id' not in stock_history and 'stock_symbol' not in stock_history:
    #     return 'stock_id or stock_symbol required'
    if 'stock_id' not in stock_history:
        return 'stock_id required'
    elif 'date' not in stock_history:
        return 'date required'
    elif 'high' not in stock_history:
        return 'high required'
    elif 'low' not in stock_history:
        return 'low required'
    elif 'open' not in stock_history:
        return 'open required'
    elif 'close' not in stock_history:
        return 'close required'


    new_history = Stock_History(
        fk_stock_id=stock_history['stock_id'],
        date=stock_history['date'],
        high=stock_history['high'],
        low=stock_history['low'],
        open=stock_history['open'],
        close=stock_history['close']
    )

    dba.session.add(new_history)
    dba.session.commit()


def _process_mockaroo_query(dataUrl, processing_function, entry_type="entries"):
    url = dataUrl + f"?key={os.environ.get('API_KEY_MOCKAROO')}"

    response = requests.get(url)

    # only add users if successful response
    if response.status_code == 200:

        json_users = response.json()

        errors = 0

        for user in json_users:
            error = processing_function(user)
            if error is not None:
                errors += 1

        users_added = len(json_users) - errors

        # return a summary and print it to console
        click.echo(f'Added {users_added} ' + entry_type + f' ({errors} errors)')
        return

    # display erroneous responses
    click.echo(response.json())