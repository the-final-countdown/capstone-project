from datetime import datetime

from database.db import db


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
