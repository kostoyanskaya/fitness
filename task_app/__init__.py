from flask import Flask
from .extensions import db, migrate, login_manager, csrf
from task_app.api.routes import api_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('task_app.settings.Config')
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    app.register_blueprint(api_bp, url_prefix='/api')

    @login_manager.user_loader
    def load_user(user_id):
        from task_app.models.user_model import User
        return User.query.get(int(user_id))

    return app
