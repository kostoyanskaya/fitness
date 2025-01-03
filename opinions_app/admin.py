from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from settings import Config
from opinions_app import app
from .models import db, User, ExerciseType, DayOfWeek, Coach, Workout, Booking, PersonalTraining, Subscription
from flask_admin.form import fields
from wtforms import PasswordField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class UserModelView(ModelView):
    column_labels = {
        'id': 'ID',
        'username': 'Имя пользователя',
        'email': 'Электронная почта',
        'date_added': 'Дата добавления',
        'telephone': 'Телефон'
    }
    column_exclude_list = ['password', 'Bookings', 'Personal Trainings']
    form_excluded_columns = ['Bookings', 'Personal Trainings']
    form_columns = ['username', 'email', 'password', 'date_added', 'telephone']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

class ExerciseTypeModelView(ModelView):
    column_labels = {
        'id': 'ID',
        'name': 'Название упражнения',
        'workouts': 'Тренировки'
    }
    form_columns = ['name']

class DayOfWeekModelView(ModelView):
    column_labels = {
        'id': 'ID',
        'name': 'Название дня',
        'workouts': 'Тренировки'
    }
    form_columns = ['name']

class CoachModelView(ModelView):
    column_labels = {
        'id': 'ID',
        'name': 'Имя тренера',
        'photo': 'Фото тренера',
        'description': 'Описание',
        'workouts': 'Тренировки'
    }
    form_columns = ['name', 'description', 'photo']


class WorkoutModelView(ModelView):
    column_labels = {
        'id': 'ID',
        'exercise_type_id': 'Тип упражнения',
        'day_of_week_id': 'День недели',
        'coach_id': 'ID Тренера',
        'date': 'Дата',
        'time': 'Время'
    }

class BookingModelView(ModelView):
    column_labels = {
        'id': 'ID',
        'user_id': 'ID пользователя',
        'workout_id': 'ID тренировки',
        'date_booked': 'Дата бронирования',
        'user': 'Пользователь',
        'workout': 'Тренировка'
    }

class PersonalTrainingModelView(ModelView):
    column_labels = {
        'id': 'ID',
        'date': 'Дата',
        'time': 'Время',
        'user_id': 'ID пользователя',
        'day_of_week_id': 'ID дня недели',
        'coach_id': 'ID тренера',
        'coach': 'Тренер',
        'day_of_week': 'День недели',
        'user': 'Пользователь'
    }

class SubscriptionModelView(ModelView):
    column_labels = {
        'id': 'ID',
        'name': 'Название подписки',
        'price': 'Цена'
    }

admin = Admin(app, name='Мой Админ', template_mode='bootstrap3')

admin.add_view(UserModelView(User, db.session, name='Пользователи'))
admin.add_view(ExerciseTypeModelView(ExerciseType, db.session, name='Типы упражнений'))
admin.add_view(DayOfWeekModelView(DayOfWeek, db.session, name='Дни недели'))
admin.add_view(CoachModelView(Coach, db.session, name='Тренеры'))
admin.add_view(WorkoutModelView(Workout, db.session, name='Тренировки'))
admin.add_view(BookingModelView(Booking, db.session, name='Записи'))
admin.add_view(PersonalTrainingModelView(PersonalTraining, db.session, name='Персональные тренировки'))
admin.add_view(SubscriptionModelView(Subscription, db.session, name='Подписки'))