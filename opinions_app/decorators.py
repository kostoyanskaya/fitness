from flask_login import current_user
from functools import wraps
from flask import Flask, request, jsonify

def role_required(role):
    """Декоратор для ограничения доступа на основе ролей."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify("Пользователь не аутентифицирован."), 401
            if not getattr(current_user, 'is_admin', False):
                return jsonify("Доступ запрещен. У вас нет разрешения на доступ к этому ресурсу."), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator