import os

from flask import redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, TextAreaField

from fitness_app import app
from .models import (db, Booking, Coach, DayOfWeek,
                     ExerciseType, PersonalTraining,
                     Price, User, Workout)

bcrypt = Bcrypt(app)


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
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
    form_columns = [
        'username',
        'email',
        'password',
        'date_added',
        'telephone',
        'is_admin'
    ]

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = (
                bcrypt.generate_password_hash(form.password.data)
                .decode('utf-8')
            )


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
            filepath = os.path.join('fitness_app', 'static', 'uploads', filename)
            form.photo.data.save(filepath)
            model.photo = os.path.join('uploads', filename)

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


class PriceModelView(AdminModelView):
    column_labels = {
        'id': 'ID',
        'name': 'Название подписки',
        'price': 'Цена'
    }


admin = Admin(app, name='Мой Админ', template_mode='bootstrap3')

admin.add_view(UserModelView(User, db.session, name='Пользователи'))
admin.add_view(ExerciseTypeModelView(
    ExerciseType, db.session, name='Типы упражнений'
    ))
admin.add_view(DayOfWeekModelView(DayOfWeek, db.session, name='Дни недели'))
admin.add_view(CoachModelView(Coach, db.session, name='Тренеры'))
admin.add_view(WorkoutModelView(Workout, db.session, name='Тренировки'))
admin.add_view(BookingModelView(Booking, db.session, name='Записи'))
admin.add_view(PersonalTrainingModelView(
    PersonalTraining, db.session, name='Персональные тренировки'
    ))
admin.add_view(PriceModelView(Price, db.session, name='Цена'))