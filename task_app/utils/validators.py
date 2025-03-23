import re

from task_app.models.user_model import User


def validate_username(username):
    """
    Validate username: only English letters and numbers are allowed.
    """
    if not re.match(r'^[A-Za-z0-9]+$', username):
        return False, 'Username must contain only English letters and numbers.'
    if User.query.filter_by(username=username).first():
        return False, 'A user with this username already exists.'
    return True, None


def validate_password(password):
    """
    Validate password: minimum 8 characters required.
    """
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long.'
    return True, None
