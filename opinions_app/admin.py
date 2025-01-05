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
from flask_admin.form.upload import FileUploadField
from werkzeug.utils import secure_filename
import os
from flask_wtf.file import FileRequired
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from flask_wtf.file import FileField, FileRequired
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, current_user
from flask import  flash, redirect, render_template, url_for
from flask.views import MethodView
from functools import wraps
from flask import abort

bcrypt = Bcrypt(app)

from functools import wraps
from flask import abort


class AdminModelView(ModelView):
    def is_accessible(self):
        # Проверяем, что пользователь аутентифицирован и является администратором
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Если пользователь не имеет доступа, перенаправляем его на главную страницу
        return redirect(url_for('index_view'))


class UserModelView(AdminModelView):

    column_labels = {
        'id': 'ID',
        'username': 'Имя пользователя',
        'email': 'Электронная почта',
        'date_added': 'Дата добавления',
        'telephone': 'Телефон',
        'is_admin': 'Администратор'
    }
    column_exclude_list = ['password', 'Bookings', 'Personal Trainings']
    form_excluded_columns = ['Bookings', 'Personal Trainings']
    form_columns = ['username', 'email', 'password', 'date_added', 'telephone', 'is_admin']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

class ExerciseTypeModelView(AdminModelView):
    column_labels = {
        'id': 'ID',
        'name': 'Название упражнения',
        'workouts': 'Тренировки'
    }
    form_columns = ['name']

class DayOfWeekModelView(AdminModelView):
    column_labels = {
        'id': 'ID',
        'name': 'Название дня',
        'workouts': 'Тренировки'
    }
    form_columns = ['name']

class CoachForm(FlaskForm):
    name = StringField('Имя тренера')
    description = TextAreaField('Описание')
    photo = FileField('Фото тренера', validators=[FileRequired()])

class CoachModelView(AdminModelView):
    form = CoachForm
    column_labels = {
        'id': 'ID',
        'name': 'Имя тренера',
        'photo': 'Фото тренера',
        'description': 'Описание',
        'workouts': 'Тренировки'
    }
    form_columns = ['name', 'description', 'photo']

    def _handle_file_upload(self, form, model):
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            filepath = os.path.join('opinions_app', 'static', filename)
            form.photo.data.save(filepath)
            model.photo = filename

    def on_model_change(self, form, model, is_created):
        self._handle_file_upload(form, model)
        super().on_model_change(form, model, is_created)



class WorkoutModelView(AdminModelView):
    column_labels = {
        'id': 'ID',
        'exercise_type_id': 'Тип упражнения',
        'day_of_week_id': 'День недели',
        'coach_id': 'ID Тренера',
        'date': 'Дата',
        'time': 'Время'
    }

class BookingModelView(AdminModelView):
    column_labels = {
        'id': 'ID',
        'user_id': 'ID пользователя',
        'workout_id': 'ID тренировки',
        'date_booked': 'Дата бронирования',
        'user': 'Пользователь',
        'workout': 'Тренировка'
    }

class PersonalTrainingModelView(AdminModelView):
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

class SubscriptionModelView(AdminModelView):
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

