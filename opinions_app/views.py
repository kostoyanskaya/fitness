from flask import  flash, redirect, render_template, url_for

from opinions_app import app, db

from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from .forms import RegistrationForm, LoginForm, WorkoutForm, BookingForm
from .models import User, Workout, Booking, ExerciseType, DayOfWeek, Coach

bcrypt = Bcrypt(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/home')
def index_view():
    """Главная страница."""
    return render_template('home.html')

@app.route('/ho')
def in_view():
    """Главная страница."""
    return render_template('proba.html')


@app.route('/admin/workout/add', methods=['GET', 'POST'])
def add_workout():
    form = WorkoutForm()
    form.exercise_type.choices = [(et.id, et.name) for et in ExerciseType.query.all()]
    form.day_of_week.choices = [(dow.id, dow.name) for dow in DayOfWeek.query.all()]
    form.coach.choices = [(c.id, c.name) for c in Coach.query.all()]

    if form.validate_on_submit():
        workout = Workout(
            exercise_type_id=form.exercise_type.data,
            day_of_week_id=form.day_of_week.data,
            coach_id=form.coach.data,
            date=form.date.data,
            time=form.time.data
        )
        db.session.add(workout)
        db.session.commit()
        flash('Тренировка успешно добавлена!', 'success')
        return redirect(url_for('book_workout'))

    return render_template('add_workout.html', form=form)

@app.route('/booking', methods=['GET', 'POST'])
def book_workout():
    form = BookingForm()
    workouts = Workout.query.all()
    workout_list = []
    for workout in workouts:
        workout_list.append({
            'day': workout.day_of_week.name,
            'date': workout.date,
            'time': workout.time,
            'exercise': workout.exercise_type.name,
            'coach': workout.coach.name,
            'id': workout.id
        })

    if form.validate_on_submit():
        booking = Booking(user_id=current_user.id, workout_id=form.workout.data)
        db.session.add(booking)
        db.session.commit()
        flash('Вы успешно записались на тренировку!', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('book_workout.html', form=form, workouts=workout_list)