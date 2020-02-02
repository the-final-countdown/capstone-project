import functools

from flask import Blueprint, request, render_template, session, redirect, url_for, flash

from db import get_db, get_user_by_email

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None

        if not email:
            error = 'Username required'
        elif not password:
            error = 'Password required'
        elif get_user_by_email(email) is not None:
            error = 'User is already registered'

        if error is None:
            db = get_db()

            db.execute(
                'INSERT INTO users (email, password) VALUES (? , ?)',
                (email, password,)
            )
            db.commit()

            return redirect(url_for('auth.login'))
        else:
            flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)

        error = None

        if user is None:
            error = 'Incorrect email'
        elif not user['password'] == password:
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))
        else:
            flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view