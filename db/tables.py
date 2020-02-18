from datetime import datetime
from db import dba
from flask_sqlalchemy import SQLAlchemy

class User(dba.Model):
    __tablename__ = 'user'
    id = dba.Column(dba.Integer, primary_key=True)
    email = dba.Column(dba.Text, unique=True, nullable=False)
    password = dba.Column(dba.Text, nullable=False)
    first_name = dba.Column(dba.Text)
    last_name = dba.Column(dba.Text)
    address = dba.Column(dba.Text)
    city = dba.Column(dba.Text)
    state = dba.Column(dba.Text)
    zip_code = dba.Column(dba.Text)
    telephone = dba.Column(dba.Text)
    created_on = dba.Column(dba.TIMESTAMP, nullable=False, default=datetime.utcnow)
    is_admin = dba.Column(dba.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}'


class Portfolio(dba.Model):
    __tablename__ = 'portfolio'
    id = dba.Column(dba.Integer, primary_key=True)
    display_name = dba.Column(dba.Text)
    created_on = dba.Column(dba.TIMESTAMP, nullable=False, default=datetime.utcnow)

    user_id = dba.Column(dba.Integer, dba.ForeignKey('user.id'), nullable=False)
    user = dba.relationship('User', backref=dba.backref('users', lazy=True))

    def __repr__(self):
        return f'<Portfolio {self.display_name} (Owned by {self.user})'

class Transaction(dba.Model):
    __tablename__ = 'transaction'
    id = dba.Column(dba.Integer, primary_key=True)
    fk_portfolio_id = dba.Column(dba.Integer, dba.ForeignKey('portfolio.id'))
    fk_stock_id = dba.Column(dba.Integer, dba.ForeignKey('stock.id'))
    number_shares = dba.Column(dba.Float, default=1)
    purchase_date = dba.Column(dba.TIMESTAMP, nullable=False, default=datetime.utcnow)
    purchase_price = dba.Column(dba.Float)
    sell_on = dba.Column(dba.TIMESTAMP, nullable=True)
    sell_price = dba.Column(dba.Float)
    transaction_finalized = dba.Column

    # @dba.hybrid_property
    # def profit_loss(self):
    #     return self.sell_price - self.purchase_price

    def __repr__(self):
        return f'<Transaction of stock {self.fk_stock_id} (Owned by portfolio {self.fk_portfolio_id})'


class Stock(dba.Model):
    __tablename__ = 'stock'
    id = dba.Column(dba.Integer, primary_key=True)
    stock_symbol = dba.Column(dba.Text, nullable=False)
    company_name = dba.Column(dba.Text, nullable=False)

    def __repr__(self):
        return f'<Stock {self.stock_symbol} (ID {self.id}): {self.company_name}'


class Stock_History(dba.Model):
    __tablename__ = 'stock_history'
    id = dba.Column(dba.Integer, primary_key=True)
    fk_stock_id = dba.Column(dba.Integer, dba.ForeignKey('stock.id'))
    date = dba.Column(dba.TIMESTAMP, nullable=False, default=datetime.utcnow)
    high = dba.Column(dba.Float)
    low = dba.Column(dba.Float)
    open = dba.Column(dba.Float)
    close = dba.Column(dba.Float)

    def __repr__(self):
        return f'<History of stock {self.fk_stock_id} (ID {self.id}) on {self.date}'