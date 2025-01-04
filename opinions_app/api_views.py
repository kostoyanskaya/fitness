from flask import Flask, jsonify, request, render_template, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .models import db, User, ExerciseType, DayOfWeek, Coach, Subscription, Workout, Booking, PersonalTraining
from opinions_app import app
from flask_login import login_user, logout_user, login_required
from flask_login import current_user
from datetime import datetime
import os
import requests
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from .schemas import UserSchema, ExerciseTypeSchema, DayOfWeekSchema, CoachSchema, SubscriptionSchema, WorkoutSchema, BookingSchema, PersonalTrainingSchema, WorkoutSchemaForUsers

bcrypt = Bcrypt(app)

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')
    confirmpassword = data.get('confirmpassword')

    existing_user = User.query.filter_by(username=fullname).first()
    if existing_user:
        return jsonify({'message': 'Имя пользователя уже существует!'}), 400
    elif password == confirmpassword:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=fullname, email=email, password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
            return jsonify({'message': 'Ваш аккаунт был создан!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Произошла ошибка при создании вашего аккаунта.'}), 500
    else:
        return jsonify({'message': 'Пароли не совпадают!'}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        user_schema = UserSchema()
        return jsonify({'message': 'Вход успешен!', 'user': user_schema.dump(user)}), 200
    else:
        return jsonify({'message': 'Вход не удался. Пожалуйста, проверьте имя пользователя и пароль!'}), 401


@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    users_list = user_schema.dump(users)
    return jsonify(users_list), 200


@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Logout successful!'}), 200


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not current_user.is_authenticated:
        return jsonify({'message': 'Нет доступа'}), 401

    user = User.query.get(user_id)
    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Пользователь успешно удален'}), 200

@app.route('/api/exercise_types', methods=['GET', 'POST'])
def handle_exercise_types():
    exercise_type_schema = ExerciseTypeSchema()

    if request.method == 'GET':
        exercise_types = ExerciseType.query.all()
        exercise_types_list = exercise_type_schema.dump(exercise_types, many=True)
        return jsonify(exercise_types_list), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        new_exercise_type = exercise_type_schema.load(data)
        exercise_type = ExerciseType(**new_exercise_type)
        db.session.add(exercise_type)
        db.session.commit()
        response = exercise_type_schema.dump(exercise_type)
        return jsonify(response), 201

@app.route('/api/exercise_types/<int:id>', methods=['DELETE'])
def delete_exercise_type(id):
    exercise_type = ExerciseType.query.get(id)
    if not exercise_type:
        abort(404)
    db.session.delete(exercise_type)
    db.session.commit()
    return jsonify({'message': 'Тип упражнения успешно удален'}), 200

@app.route('/api/days_of_week', methods=['GET', 'POST'])
def handle_days_of_week():
    day_of_week_schema = DayOfWeekSchema()

    if request.method == 'GET':
        days_of_week = DayOfWeek.query.all()
        days_list = day_of_week_schema.dump(days_of_week, many=True)
        return jsonify(days_list), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_day_of_week = day_of_week_schema.load(data)
        day_of_week = DayOfWeek(**new_day_of_week)
        db.session.add(day_of_week)
        db.session.commit()
        return jsonify(day_of_week_schema.dump(day_of_week)), 201 

@app.route('/api/days_of_week/<int:id>', methods=['DELETE'])
def delete_day_of_week(id):
    day_of_week = DayOfWeek.query.get(id)
    if not day_of_week:
        abort(404)
    db.session.delete(day_of_week)
    db.session.commit()
    return jsonify({'message': 'День недели успешно удален'}), 200

@app.route('/api/coaches', methods=['GET', 'POST'])
def handle_coaches():
    coach_schema = CoachSchema()

    if request.method == 'GET':
        coaches = Coach.query.all()
        coaches_list = coach_schema.dump(coaches, many=True)
        return jsonify(coaches_list), 200

    elif request.method == 'POST':
        data = request.get_json()
        photo_url = data.get('photo')
        photo_path = None

        if photo_url:
            try:
                response = requests.get(photo_url)
                if response.status_code == 200:
                    filename = secure_filename(os.path.basename(photo_url))
                    static_dir = os.path.join('opinions_app', 'static')
                    if not os.path.exists(static_dir):
                        os.makedirs(static_dir)
                    
                    filepath = os.path.join(static_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    photo_path = filename
                else:
                    return jsonify({'error': 'Не удалось загрузить изображение'}), 400
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        new_coach_data = coach_schema.load(data)
        new_coach = Coach(name=new_coach_data['name'], description=new_coach_data.get('description'), photo=photo_path)
        db.session.add(new_coach)
        db.session.commit()

        return jsonify(coach_schema.dump(new_coach)), 201

@app.route('/api/coaches/<int:id>', methods=['DELETE'])
def delete_coach(id):
    coach = Coach.query.get(id)
    if not coach:
        abort(404)
    db.session.delete(coach)
    db.session.commit()
    return jsonify({'message': 'Coach deleted successfully'}), 200

@app.route('/api/subscriptions', methods=['GET', 'POST'])
def handle_subscriptions():
    subscription_schema = SubscriptionSchema()
    
    if request.method == 'GET':
        subscriptions = Subscription.query.all()
        return jsonify(subscription_schema.dump(subscriptions, many=True)), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_subscription = subscription_schema.load(data)
        db.session.add(new_subscription)
        db.session.commit()
        return subscription_schema.dump(new_subscription), 201

@app.route('/api/subscriptions/<int:id>', methods=['DELETE'])
def delete_subscription(id):
    subscription = Subscription.query.get(id)
    if not subscription:
        abort(404)
    db.session.delete(subscription)
    db.session.commit()
    return jsonify({'message': 'Subscription deleted successfully'}), 200


@app.route('/api/workouts', methods=['GET', 'POST'])
def handle_workouts():
    workout_schema = WorkoutSchema()
    
    if request.method == 'GET':
        workout_schema_get = WorkoutSchemaForUsers()
        workouts = Workout.query.all()
        return jsonify(workout_schema_get.dump(workouts, many=True)), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_workout = workout_schema.load(data)
        db.session.add(new_workout)
        db.session.commit()
        return workout_schema.dump(new_workout), 201

@app.route('/api/bookings', methods=['POST'])
def book_workouts():
    booking_schema = BookingSchema()
    data = request.get_json()
    new_booking = booking_schema.load(data)

    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Successfully booked workout.', 'booking_id': new_booking.id}), 201

@app.route('/api/personal_trainings', methods=['POST'])
@login_required
def book_personal_training():
    personal_training_schema = PersonalTrainingSchema()
    data = request.get_json()
    data['user_id'] = current_user.id
    data['workout_type'] = "Персональная тренировка"
    coach = Coach.query.get(data['coach_id'])
    if not coach or not coach.workouts:
        return jsonify({'error': 'Тренер не найден или у него нет доступных типов тренировок.'}), 404
    new_training = personal_training_schema.load(data)
    db.session.add(new_training)  
    db.session.commit()

    return jsonify({
        'message': 'Успешно записано на персональную тренировку.',
        'personal_training_id': new_training.id
    }), 201

@app.route('/api/user/trainings', methods=['GET'])
def get_user_trainings():
    if current_user.is_authenticated:
        bookings = Booking.query.filter_by(user_id=current_user.id).all()

        workout_schema = WorkoutSchemaForUsers(many=True)
        workouts = []
        for booking in bookings:
            workout = Workout.query.get(booking.workout_id)
            workouts.append(workout)

        workouts_data = workout_schema.dump(workouts)

        personal_workouts = PersonalTraining.query.filter_by(user_id=current_user.id).all()
        personal_training_schema = PersonalTrainingSchema(many=True)
        personal_workouts_data = personal_training_schema.dump(personal_workouts)

        return jsonify({
            'workouts': workouts_data,
            'personal_workouts': personal_workouts_data
        }), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/api/bookings/<int:workout_id>', methods=['DELETE'])
@login_required
def cancel_booking(workout_id):
    booking = Booking.query.filter_by(workout_id=workout_id, user_id=current_user.id).first()
    if not booking:
        return jsonify({'message': 'Booking not found.'}), 404
    db.session.delete(booking)
    db.session.commit()

    return jsonify({'message': 'Booking cancelled successfully.', 'status': 'success'}), 200

@app.route('/api/cancel_personal_booking/<int:personal_booking_id>', methods=['DELETE'])
def cancel_personal_booking(personal_booking_id):
    if current_user.is_authenticated:
        personal_booking = PersonalTraining.query.filter_by(id=personal_booking_id, user_id=current_user.id).first()
        if personal_booking:
            db.session.delete(personal_booking)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Персональная тренировка отменена.'}), 200
        return jsonify({'status': 'error', 'message': 'Персональная тренировка не найдена.'}), 404
    return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_admin = User(username=username, password=password, is_admin=True)
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('create_admin.html')