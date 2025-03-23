from task_app.models.user_model import User
from task_app.schemas.user_schema import UserSchema
from task_app.utils.validators import validate_username, validate_password


class UserService:
    @staticmethod
    def get_users(logged_in=False):
        """Get a list of all users."""
        users = User.query.all()
        user_schema = UserSchema(many=True)
        if logged_in:
            return user_schema.dump(users)
        return [user.username for user in users]

    @staticmethod
    def api_login_user(username, password):
        """Authenticate a user."""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def register_user(username, password, full_name, gender, birth_date):
        """Register a new user."""
        is_valid, error_message = validate_username(username)
        if not is_valid:
            return {'error': error_message}, 400
        is_valid, error_message = validate_password(password)
        if not is_valid:
            return {'error': error_message}, 400
        new_user = User(
            username=username,
            full_name=full_name,
            gender=gender,
            birth_date=birth_date
        )
        new_user.set_password(password)
        return new_user
