import functools

from flask import Blueprint, request, render_template, session, g, redirect, url_for, flash
from werkzeug.security import check_password_hash

import db

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        db.create_user({
            'first-name': request.form.get('first-name'),
            'last-name': request.form.get('last-name'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
        })
        return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html')

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.get_user_by_email(email)

        error = None

        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        # redirect if credentials are correct
        if error is None:
            session.clear()
            session['user_id'] = user.id

            return redirect(url_for('index'))

        # flash error on incorrect credentials
        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.get_user_by_id(user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
