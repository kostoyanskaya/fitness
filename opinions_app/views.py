from flask import  flash, redirect, render_template, url_for, request, session

from opinions_app import app, db

from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from .forms import RegistrationForm, LoginForm, WorkoutForm, BookingForm, PersonalTrainingForm
from .models import User, Workout, Booking, ExerciseType, DayOfWeek, Coach, PersonalTraining, Subscription


bcrypt = Bcrypt(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        existing_user = User.query.filter_by(username=fullname).first()
        
        if existing_user:
            flash('Username already exists! Please choose a different one.', 'danger')
        elif password == confirmpassword:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=fullname, email=email, password=hashed_password)
            print(user)
            db.session.add(user)
            try:
                db.session.commit()
                flash('Your account has been created! You can now log in.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating your account. Please try again.', 'danger')
        else:
            flash('Passwords do not match!', 'danger')

    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('me_view'))
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('me_view'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('me_view'))



@app.route('/home')
def index_view():
    """Главная страница."""
    return render_template('home.html')


@app.route('/me')
def me_view():
    if current_user.is_authenticated:
        bookings = Booking.query.filter_by(user_id=current_user.id).all()
        workout_details = []

        for booking in bookings:
            workout = booking.workout
            workout_details.append({
                'date': workout.date.strftime('%d.%m.%Y'),
                'time': workout.time.strftime('%H:%M'),
                'exercise': workout.exercise_type.name,
                'coach': workout.coach.name,
                'id': booking.id
            })

        personal_trainings = PersonalTraining.query.filter_by(user_id=current_user.id).all()
        personal_workout_details = []

        for personal_workout in personal_trainings:
            personal_workout_details.append({
                'date': personal_workout.date.strftime('%d.%m.%Y'),
                'time': personal_workout.time.strftime('%H:%M'),
                'exercise': 'Персональная тренировка',
                'coach': personal_workout.coach.name,
                'id': personal_workout.id
            })

        return render_template('person.html', username=current_user.username,
                               email=current_user.email,
                               workouts=workout_details,
                               personal_workouts=personal_workout_details)
    else:
        return redirect(url_for('login'))
    
@app.route('/cancel_booking/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking and booking.user_id == current_user.id:
        db.session.delete(booking)
        db.session.commit()
        flash('Запись на тренировку отменена.', 'success')
    else:
        flash('Не удалось отменить запись.', 'danger')
    
    return redirect(url_for('me_view'))

@app.route('/cancel_personal_booking/<int:booking_id>', methods=['POST'])
def cancel_personal_booking(booking_id):
    personal_training = PersonalTraining.query.get(booking_id)
    if personal_training and personal_training.user_id == current_user.id:
        db.session.delete(personal_training)
        db.session.commit()
        flash('Персональная тренировка отменена.', 'success')
    else:
        flash('Не удалось отменить тренировку.', 'danger')
    return redirect(url_for('me_view'))



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

    if request.method == 'POST':
        workout_id = request.form.get('workout')
        booking = Booking(user_id=current_user.id, workout_id=workout_id)
        db.session.add(booking)
        db.session.commit()
        flash('Вы успешно записались на тренировку!', 'success')
        return redirect(url_for('book_workout'))

    return render_template('book_workout.html', workouts=workout_list)


@app.route('/teacher', methods=['GET', 'POST'])
def teacher_view():
    """Тренер страница."""
    coaches = Coach.query.all()
    form = PersonalTrainingForm()
    if request.method == 'POST':
        form.process(formdata=request.form)

        if form.validate_on_submit():
            selected_date = form.date.data
            day_of_week_id = selected_date.weekday()
            coach_id = request.form.get('coach_id')
            user_id = current_user.id
            new_booking = PersonalTraining(
                day_of_week_id=day_of_week_id,
                coach_id=coach_id,
                date=form.date.data,
                time=form.time.data,
                user_id=user_id
            )

            db.session.add(new_booking)
            db.session.commit()

            flash('Вы успешно записаны на занятие!', 'success')
            return redirect(url_for('teacher_view'))
        else:
            app.logger.error(f"Form errors: {form.errors}")

    return render_template('my_teacher.html', coaches=coaches, form=form)

@app.route('/contacts')
def information_view():
    """Контакты."""
    return render_template('contacts.html')

@app.route('/price')
def price_view():
    """Ценообразование."""
    subscriptions = Subscription.query.all()  # Получаем все абонементы из базы данных
    return render_template('cost.html', subscriptions=subscriptions)

