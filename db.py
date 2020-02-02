import sqlite3

from flask import current_app, g
from flask.cli import with_appcontext

# allows for command line interfacing
import click


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # run queries in schema.sql
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    init_db()


# ~~~~~~~~~~~~~~~~~~~ QUERIES ~~~~~~~~~~~~~~~~~~~


def get_user_by_id(user_id):
    """
    Get the user by their id

    :param user_id: the id of the user
    :return: the user or None
    """
    return get_db().execute(
        'SELECT * FROM users WHERE id = ?',
        (user_id,)
    ).fetchone()


def get_user_by_email(email):
    """
    Get the user by their id

    :param user_id: the id of the user
    :return: the user or None
    """
    return get_db().execute(
        'SELECT * FROM users WHERE email = ?',
        (email,)
    ).fetchone()


def get_all_users(**kwargs):
    """
    Returns all users meeting the criteria passed in **kwargs.

    # Usage
    get_all_users(state='NC') returns all results from the query:
    SELECT * FROM users WHERE state = 'NC'

    :param kwargs: the key/value pairs that correspond to columns in the user database
    :return: all results meeting the criteria passed in **kwargs.
    """
    return get_db().execute(
        'SELECT * FROM users'
    ).fetchall()