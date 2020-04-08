import os
import requests
import click
import random
import csv
# from datetime import datetime

from flask import jsonify
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


dba = SQLAlchemy()

from db.tables import *
from db import stock_handler as sth
import json

print_log = ""

def init_app(app):
    with app.app_context():
        dba.init_app(app)
        dba.create_all()

        # Adding click commands:
        app.cli.add_command(click_first_run)
        app.cli.add_command(clear_db)
        app.cli.add_command(click_populate_db)
        app.cli.add_command(click_populate_users)
        app.cli.add_command(click_populate_stocks)
        app.cli.add_command(click_clean_stocks)
        app.cli.add_command(click_populate_stock_history)
        app.cli.add_command(click_generate_portfolios)

        # first_run()


        # populate_users()

@click.command('first-run')
@with_appcontext
def click_first_run():
    first_run()

def first_run():
    initial_startup_check: Internal_Startup = Internal_Startup.query.filter(
        Internal_Startup.id == 0).first()
    if not (initial_startup_check is None) and initial_startup_check.complete:
        print("Has run before. skipping first run...")
        return


    click.echo("Performing first run...")

    if initial_startup_check is None:
        dba.session.add(Internal_Startup(
                id=0,
                complete=False
            )
        )

    create_user({
       'first-name': "The",
       'last-name': "Admin",
       'email': "admin@tfc.com",
       'password': "IAmTheAdmin!!1",
    })

    # populate_db()
    get_user_by_email("admin@tfc.com").is_admin = True

    Internal_Startup.query.filter(Internal_Startup.id == 0).first().complete=True

    dba.session.commit()
    click.echo("First run complete!")



@click.command('clear-db')
@with_appcontext
def click_clear_db():
    clear_db()

def clear_db(current_user: User = None):
    Transaction.query.delete()
    Portfolio.query.delete()
    Stock.query.delete()
    Stock_History.query.delete()
    Internal_Startup.query.delete()

    if not current_user is None:
        User.query.filter(User.id!=current_user.id).delete()
    else:
        User.query.delete()

    dba.session.commit()

    print("DB Cleared")




@click.command('populate-db')
@with_appcontext
def click_populate_db():
    populate_db()


def populate_db():
    populate_users()
    populate_stocks()
    # clean_stocks()
    # populate_stock_history()
    populate_and_clean_stock_history()
    generate_portfolios()
    click.echo("population complete!")

@click.command('populate-users')
@with_appcontext
def click_populate_users():
    populate_users()

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
def click_populate_stocks():
    populate_stocks()

def populate_stocks():
    _process_mockaroo_query("https://my.api.mockaroo.com/stock_symbols.json", create_stock, "stocks")


@click.command('clean-stock-data')
@with_appcontext
def click_clean_stocks():
    clean_stocks()

def clean_stocks():
    to_remove = []

    stockList = dba.engine.execute("SELECT * FROM STOCK").fetchall()
    stockTotal = len(stockList)
    stockIter = 0

    for stock in stockList:
        stockIter += 1
        click.echo(f"Stock {stockIter} of {stockTotal}: ")

        rId = stock[0]
        rSymbol = stock[1]
        rName = stock[2]

        history = sth.fetch_stock_data(rSymbol)

        # if history.

        if len(history.index) <= 0:
            click.echo(rSymbol + " not found. Removing... ")
            to_remove.append(rId)
        else:
            click.echo("Found " + rSymbol + "... ")

    for id in to_remove:
        dba.engine.execute(f"DELETE FROM STOCK WHERE ID = {id}")
        dba.session.commit()
    click.echo("All unfound stocks removed!")


@click.command('populate-stock-data')
@with_appcontext
def click_populate_stock_history():
    populate_stock_history()

def populate_stock_history():
    stockList = dba.engine.execute("SELECT * FROM STOCK").fetchall()
    stockTotal = len(stockList)
    stockIter = 0

    for stock in stockList:
        stockIter += 1
        click.echo(f"Stock {stockIter} of {stockTotal}: ")

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


@click.command('populate-and-clean-stock-data')
@with_appcontext
def click_populate_and_clean_stock_history():
    populate_and_clean_stock_history()

def populate_and_clean_stock_history():
    to_remove = []

    stockList = dba.engine.execute("SELECT * FROM STOCK").fetchall()
    stockTotal = len(stockList)
    stockIter = 0

    for stock in stockList:
        stockIter += 1
        click.echo(f"Stock {stockIter} of {stockTotal}: ")

        rId = stock[0]
        rSymbol = stock[1]
        rName = stock[2]

        history = sth.fetch_stock_data(rSymbol)

        # if history.

        if len(history.index) <= 0:
            click.echo(rSymbol + " not found. Skipping... ")
            to_remove.append(rId)
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

    for id in to_remove:
        dba.engine.execute(f"DELETE FROM STOCK WHERE ID = {id}")
        dba.session.commit()
    click.echo("All unfound stocks removed!")
    # dba.session.commit()

@click.command('generate-portfolios')
@with_appcontext
def click_generate_portfolios():
    generate_portfolios()

def generate_portfolios():
    for user in dba.engine.execute("SELECT * FROM USER").fetchall():
        # click.echo(user)

        num_of_portfolios = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3])

        for i in range(1, num_of_portfolios + 1):
            display_name = f"{user[3]} {user[4]} Portfolio {i}"

            click.echo(f"generating {display_name}...")

            fill_portfolio(create_portfolio_params(user[0], display_name).id)



def fill_portfolio(portfolio_id: int):
    num_of_stocks = random.randint(1, 6)

    stock_list = get_all_stocks()

    used_stocks = []

    for i in range(0, num_of_stocks):
        selected_stock: Stock = None

        while selected_stock in used_stocks or selected_stock is None:
            selected_stock = random.choice(stock_list)
        used_stocks.append(selected_stock)

        # I can make the transaction record fancier tomorrow...
        most_recent_history: Stock_History = Stock_History.query.filter(Stock_History.fk_stock_id == selected_stock.id)\
            .order_by(Stock_History.date.desc()).first()

        print(selected_stock.stock_symbol)
        print(most_recent_history.date)

        create_transaction_params(portfolio_id, selected_stock.id, random.randint(1, 4), most_recent_history.date, most_recent_history.close, None, None)


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

    make_admin = False

    if len(User.query.all()) <= 0:
        make_admin = True

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
        telephone=user.get('telephone', None),
        is_admin=make_admin
    )

    dba.session.add(new_user)
    dba.session.commit()

    return new_user


def get_user_by_id(user_id) -> User:
    """
    Get the user by their id

    :param user_id: the id of the user
    :return: the user or None
    """
    return User.query.filter(User.id == user_id).first()


def get_user_by_email(email) -> User:
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

# def get_user_transactions(portfolio_id: int):
#     """
#     Returns all users portfolios and transactions:
#     """
#
#     retVal = {}
#
#     for pf in Portfolio.query.filter(Portfolio.user_id==user_id).all():
#
# Transaction.query.filter(Transaction.fk_portfolio_id==pf.id).all()
#
#     return retVal


def get_all_stocks():
    """
    Returns all users
    """
    return Stock.query.order_by(Stock.stock_symbol).all()

def get_stock_by_symbol(p_stock_symbol: str):
    return Stock.query.filter(Stock.stock_symbol==p_stock_symbol).first()

def get_stock_by_id(p_stock_id: int):
    return Stock.query.filter(Stock.id==p_stock_id).first()

def create_stock(stock):

    if 'stock_symbol' not in stock:
        return 'Stock symbol required'

    if len(Stock.query.filter(Stock.stock_symbol==stock['stock_symbol']).all()) > 0:
        return 'Stock already in db. Skipping...'

    stock_name = ""
    if 'stock_name' not in stock:
        stock_name = sth.get_company_name_for_symbol(stock['stock_symbol'])
    else:
        stock_name = stock['stock_name']

    new_stock = Stock(stock_symbol=stock['stock_symbol'], company_name=stock_name)

    dba.session.add(new_stock)
    dba.session.commit()

    return new_stock

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

    return new_history


def create_portfolio(portfolio_data):
    if 'user_id' not in portfolio_data:
        return 'user_id required'
    if 'display_name' not in portfolio_data:
        return 'display_name required'
    if 'created_on' not in portfolio_data:
        portfolio_data['created_on'] = datetime.now()

    return create_portfolio_params(portfolio_data['user_id'], portfolio_data['display_name'], portfolio_data['created_on'])


def create_portfolio_params(p_user_id: int, p_display_name: str, p_created_on: datetime = datetime.now()):

    new_portfolio = Portfolio(
        user_id = p_user_id,
        created_on = p_created_on,
        display_name = p_display_name
    )

    dba.session.add(new_portfolio)
    dba.session.commit()

    return new_portfolio

def create_transaction_params(p_portfolio_id: int, p_stock_id: int, p_shares: float, p_purchase_date: datetime,
                              p_purchase_price: float, p_sell_date: datetime, p_sell_price: float):

    new_transaction = Transaction(
        fk_portfolio_id=p_portfolio_id,
        fk_stock_id=p_stock_id,
        number_shares=p_shares,
        purchase_date=p_purchase_date,
        purchase_price=p_purchase_price,
        sell_on=p_sell_date,
        sell_price=p_sell_price
    )

    dba.session.add(new_transaction)
    dba.session.commit()

    return new_transaction

def _process_mockaroo_query(dataUrl, processing_function, entry_type="entries"):
    url = dataUrl + f"?key={os.environ.get('API_KEY_MOCKAROO')}"

    response = requests.get(url)

    # only add users if successful response
    if response.status_code == 200:

        json_users = response.json()

        errors = 0

        for user in json_users:
            error = processing_function(user)
            if isinstance(error, str):
                errors += 1

        users_added = len(json_users) - errors

        # return a summary and print it to console
        click.echo(f'Added {users_added} ' + entry_type + f' ({errors} errors)')
        return

    # display erroneous responses
    click.echo(response.json())

# def _lprint(message):
#     global print_log
#     click.echo(message)
#     print(message)
#     print_log += message + "\n"