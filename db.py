import os
import requests
import click
from datetime import datetime

from flask import jsonify
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import csv
from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import yfinance as yf
from random import random

db = SQLAlchemy()

def init_app(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()
        populate_users()
        create_stocks()

def populate_users():
    with open('MOCK_DATA.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            create_user(row)
        
#Models
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
    portfolio = db.relationship('Portfolio', backref='port', lazy=True)


    def __repr__(self):
        return f'<User {self.email}'

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(80), unique=False)
    stock_symbol = db.Column(db.String(10), unique=False)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.Text)
    created_on = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



# Queries
def create_stocks():
    with open('STOCK_DATA.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            db.session.add(Stock(stock_name=row['stock_name'], stock_symbol=row['stock_symbol']))
            db.session.commit()

def create_user(user):
    new_user = User(
        email=user['email'],
        password=generate_password_hash(user['password']),
        first_name=user['first_name'],
        last_name=user['last_name'],
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