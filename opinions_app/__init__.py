from flask import Flask
from settings import Config
from .extensions import db, migrate, login_manager
import os

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


from .models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from . import api_views, cli_commands, error_handlers, views, admin