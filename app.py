import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from models import User


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/add")
def add_user():
    email = request.args.get('email')
    password = request.args.get('password')
    try:
        user = User(
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return "Book added. user id={}".format(user.id)
    except Exception as e:
        return str(e)


@app.route("/users")
def view_users():
    users = User.query.all()
    return jsonify([e.serialize() for e in users])


if __name__ == '__main__':
    app.run()
