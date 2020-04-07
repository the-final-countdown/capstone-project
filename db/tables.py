from datetime import datetime
from db import dba
from flask_sqlalchemy import SQLAlchemy
import json

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


    def get_portfolios(self):
        return Portfolio.query.filter(Portfolio.user_id==self.id).all()

    def get_portfolio_by_name(self, display_name: str):
        return Portfolio.query.filter(Portfolio.user_id==self.id, Portfolio.display_name==display_name).first()

    def get_portfolio_by_id(self, this_id: int):
        return Portfolio.query.filter(Portfolio.user_id==self.id, Portfolio.id==this_id).first()


class Portfolio(dba.Model):
    __tablename__ = 'portfolio'
    id = dba.Column(dba.Integer, primary_key=True)
    display_name = dba.Column(dba.Text)
    # display_name = dba.Column(dba.Text, unique=True)
    created_on = dba.Column(dba.TIMESTAMP, nullable=False, default=datetime.utcnow)

    user_id = dba.Column(dba.Integer, dba.ForeignKey('user.id'), nullable=False)
    user = dba.relationship('User', backref=dba.backref('users', lazy=True))

    def __repr__(self):
        return f'<Portfolio {self.display_name} (Owned by {self.user})'


    # def get_link_name(self):
    #     return self.display_name.replace(" ", "_")

    def get_transactions(self):
        return Transaction.query.filter(Transaction.fk_portfolio_id == self.id).all()


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
    transaction_finalized = dba.Column(dba.BOOLEAN, default=False)

    # @dba.hybrid_property
    # def profit_loss(self):
    #     return self.sell_price - self.purchase_price

    def __repr__(self):
        return json.dumps(self.ToDict())

    def get_stock(self):
        return Stock.query.filter(Stock.id==self.fk_stock_id).first()

    def get_portfolio(self):
        return Portfolio.query.filter(Portfolio.id==self.fk_portfolio_id).first()

    def ToDict(self):
        return {
            'id': self.id,
            'fk_portfolio_id': self.fk_portfolio_id,
            'fk_stock_id': self.fk_stock_id,
            'number_shares': self.number_shares,
            'purchase_date': str(self.purchase_date),
            'purchase_price': self.purchase_price,
            'sell_on': str(self.sell_on),
            'sell_price': self.sell_price,
            'transaction_finalized': self.transaction_finalized
        }


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