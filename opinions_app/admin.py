from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from settings import Config
from opinions_app import app
from .models import db, ExerciseType, DayOfWeek
