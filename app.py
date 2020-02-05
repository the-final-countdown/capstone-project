import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/add")
def add_user():
    email = request.args.get('email')
    password = request.args.get('password')
    timestamp = request.args.get('timestamp')
    try:
        user = User(
            email=email,
            password=password,
            timestamp=timestamp
        )
        db.session.add(user)
        db.session.commit()
        return "Book added. user id={}".format(user.id)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
