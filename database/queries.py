from database.db import db
from database.models import User


def create_user(first_name, last_name, email, password):
    """
    Verifies input and returns any errors.  If there aren't any errors,
    create the user.

    :return: An error message (if applicable) or None
    """
    if first_name is None:
        return 'First name required'
    elif last_name is None:
        return 'Last name required'
    elif email is None:
        return 'Email required'
    elif get_user_by_email(email) is not None:
        return 'This email address is already registered'
    elif password is None:
        return 'Password required'

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )

    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    """
    Get the user by their id

    :param user_id: the id of the user
    :return: the user or None
    """
    return db.session.query(User).filter(User.id == user_id).first()


def get_user_by_email(email):
    """
    Get the user by their id

    :param email: the email address of the user
    :return: the user or None
    """
    return db.session.query(User).filter(User.email == email).first()


def get_all_users():
    """
    Returns all users
    """
    return db.session.query(User).all()
