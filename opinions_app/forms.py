from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms import Form, StringField


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class WorkoutForm(FlaskForm):
    exercise_type = SelectField('Тип упражнения', coerce=int, validators=[DataRequired()])
    day_of_week = SelectField('День недели', coerce=int, validators=[DataRequired()])
    coach = SelectField('Тренер', coerce=int, validators=[DataRequired()])
    date = DateField('Дата', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Время', validators=[DataRequired()])
    submit = SubmitField('Добавить тренировку')


class BookingForm(FlaskForm):
    workout = SelectField('Выберите тренировку', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Записаться')

class ExerciseTypeForm(Form):
    name = StringField('Name', validators=[DataRequired()]) 