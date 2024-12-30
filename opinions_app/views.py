from flask import  flash, redirect, render_template, url_for, request, session

from opinions_app import app, db

from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from .forms import RegistrationForm, LoginForm, WorkoutForm, BookingForm, PersonalTrainingForm
from .models import User, Workout, Booking, ExerciseType, DayOfWeek, Coach, PersonalTraining, Subscription
from werkzeug.utils import secure_filename


bcrypt = Bcrypt(app)


@app.route('/register')
def register():
    return render_template('login.html')


@app.route('/home')
def index_view():
    """Главная страница."""
    return render_template('home.html')


@app.route('/me')
def me_view():
    if current_user.is_authenticated:
        return render_template('person.html')
    else:
        return redirect(url_for('register'))
    

@app.route('/booking')
def book_workout():
    workouts = Workout.query.all()
    return render_template('book_workout.html', workouts=workouts)


@app.route('/teacher')
def teacher_view():
    """Тренер страница."""
    coaches = Coach.query.all()
    return render_template('my_teacher.html', coaches=coaches)

@app.route('/contacts')
def information_view():
    """Контакты."""
    return render_template('contacts.html')

@app.route('/price')
def price_view():
    """Ценообразование."""
    subscriptions = Subscription.query.all()
    return render_template('cost.html', subscriptions=subscriptions)

