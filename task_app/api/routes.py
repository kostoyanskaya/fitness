from flask import Blueprint
from flask_restful import Api

from task_app.controllers.user_controller import (
    GetCSRFToken,
    GetUsers,
    LoginUser,
    LogoutUser,
    RegisterUser
)

api_bp = Blueprint('api', __name__)

api = Api(api_bp)

api.add_resource(RegisterUser, '/register_user')
api.add_resource(LoginUser, '/login_user')
api.add_resource(LogoutUser, '/logout_user')
api.add_resource(GetUsers, '/get_users')
api.add_resource(GetCSRFToken, '/get_csrf')
