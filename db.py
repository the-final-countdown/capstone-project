import os
import requests
import click
from datetime import datetime

from flask import jsonify
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


def init_app(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        app.cli.add_command(populate_users)


@click.command('populate-db')
@with_appcontext
def populate_users():
    url = f"https://my.api.mockaroo.com/users.json?key={os.environ.get('API_KEY_MOCKAROO')}"

    response = requests.get(url)

    # only add users if successful response
    if response.status_code == 200:

        json_users = response.json()

        errors = 0

        for user in json_users:
            error = create_user(user)
            if error is not None:
                errors += 1

        users_added = len(json_users) - errors

        # return a summary and print it to console
        click.echo(f'Added {users_added} users ({errors} errors)')
        return

    # display erroneous responses
    click.echo(response.json())


# Models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zip_code = db.Column(db.Text)
    telephone = db.Column(db.Text)
    created_on = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}'


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.Text)
    created_on = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<Portfolio {self.display_name} (Owned by {self.user})'


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

    db.session.add(new_user)
    db.session.commit()


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