import re

from flask import jsonify

from .models import User


def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.match(r'^[A-Za-z0-9]+$', password):
        return False
    return True


def validate_registration_data(fullname, email, password, confirmpassword):
    if not fullname or not password or not email:
        return 'Имя, пароль и адрес почты обязательны!', 400
    if User.query.filter_by(username=fullname).first():
        return 'Имя пользователя уже существует!', 400
    if User.query.filter_by(email=email).first():
        return 'Адрес электронной почты уже используется!', 400
    if password != confirmpassword:
        return 'Пароли не совпадают!', 400
    if not validate_password(password):
        return 'Пароль должен содержать минимум 8 символов, включая хотя бы одну цифру и не должен содержать специальных символов.', 400
    return None