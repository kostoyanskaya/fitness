from flask import  flash, redirect, render_template, url_for, request, session

from opinions_app import app, db

from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from .forms import RegistrationForm, LoginForm, WorkoutForm, BookingForm, PersonalTrainingForm
from .models import User, Workout, Booking, ExerciseType, DayOfWeek, Coach, PersonalTraining


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
        return redirect(url_for('home'))
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index_view'))
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
        # Получаем все тренировки, на которые записан пользователь
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

        return render_template('person.html', username=current_user.username, email=current_user.email, workouts=workout_details)
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
    form = BookingForm()  # Возможно, вам не нужно использовать этот объект формы.
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
    
    if form.validate_on_submit():
        new_booking = PersonalTraining(
            exercise_type_id=form.exercise_type_id.data,
            day_of_week_id=form.day_of_week_id.data,
            coach_id=form.coach_id.data,
            date=form.date.data,
            time=form.time.data
        )
        db.session.add(new_booking)
        db.session.commit()
        flash('Вы успешно записаны на занятие!', 'success')

    return render_template('my_teacher.html', coaches=coaches, form=form)