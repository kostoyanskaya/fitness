from flask import jsonify, request
from flask_login import current_user, login_user, logout_user
from flask_restful import Resource
from flask_wtf.csrf import generate_csrf

from task_app.models.user_model import db
from task_app.schemas.user_schema import LoginSchema, UserSchema
from task_app.services.user_service import UserService


class RegisterUser(Resource):
    def post(self):
        """User registration."""
        data = request.get_json()
        schema = UserSchema()
        errors = schema.validate(data)
        if errors:
            return {'error': errors}, 400
        user_data = schema.load(data)
        result = UserService.register_user(**user_data)
        if isinstance(result, tuple):
            return result[0], result[1]
        db.session.add(result)
        db.session.commit()
        return {'message': 'User successfully registered'}, 201


class GetCSRFToken(Resource):
    def get(self):
        """Get CSRF token."""
        return jsonify({'csrf_token': generate_csrf()})


class LoginUser(Resource):
    def post(self):
        """User login."""
        data = request.get_json()
        schema = LoginSchema()
        errors = schema.validate(data)
        if errors:
            return {'error': errors}, 400
        validated_data = schema.load(data)
        username = validated_data['username']
        password = validated_data['password']
        user = UserService.api_login_user(username, password)
        if user:
            login_user(user)
            return {'message': 'Login successful'}, 200
        return {'error': 'Invalid username or password'}, 401


class LogoutUser(Resource):
    def post(self):
        """User logout."""
        logout_user()
        return {'message': 'Logout successful'}, 200


class GetUsers(Resource):
    def get(self):
        """Get list of users."""
        users = UserService.get_users(logged_in=current_user.is_authenticated)
        return users, 200
