from flask import Flask, jsonify, request, render_template, flash, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .models import db, User, ExerciseType, DayOfWeek, Coach, Subscription, Workout
from opinions_app import app
from flask_login import login_user, logout_user, login_required
from flask_login import current_user
from datetime import datetime

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
        return jsonify({'message': 'Username already exists!'}), 400
    elif password == confirmpassword:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=fullname, email=email, password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
            return jsonify({'message': 'Your account has been created!'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'An error occurred while creating your account.'}), 500
    else:
        return jsonify({'message': 'Passwords do not match!'}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)  
        return jsonify({'message': 'Login successful!', 'user': {'username': user.username, 'email': user.email}}), 200
    else:
        return jsonify({'message': 'Login Unsuccessful. Please check username and password!'}), 401

    
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]  # Формируем список пользователей
    return jsonify(users_list), 200


@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'Logout successful!'}), 200


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized'}), 401

    user = User.query.get(user_id)
    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/api/exercise_types', methods=['GET', 'POST'])
def handle_exercise_types():
    if request.method == 'GET':
        exercise_types = ExerciseType.query.all()
        exercise_types_list = [{'id': et.id, 'name': et.name} for et in exercise_types]
        return jsonify(exercise_types_list), 200
    
    elif request.method == 'POST':
        data = request.get_json()
        new_exercise_type = ExerciseType(name=data['name'])
        db.session.add(new_exercise_type)
        db.session.commit()
        return jsonify({'id': new_exercise_type.id, 'name': new_exercise_type.name}), 201

@app.route('/api/exercise_types/<int:id>', methods=['DELETE'])
def delete_exercise_type(id):
    exercise_type = ExerciseType.query.get(id)
    if not exercise_type:
        abort(404)
    db.session.delete(exercise_type)
    db.session.commit()
    return jsonify({'message': 'Exercise type deleted successfully'}), 200

@app.route('/api/days_of_week', methods=['GET', 'POST'])
def handle_days_of_week():
    if request.method == 'GET':
        days_of_week = DayOfWeek.query.all()
        days_list = [{'id': dow.id, 'name': dow.name} for dow in days_of_week]
        return jsonify(days_list), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_day_of_week = DayOfWeek(name=data['name'])
        db.session.add(new_day_of_week)
        db.session.commit()
        return jsonify({'id': new_day_of_week.id, 'name': new_day_of_week.name}), 201

@app.route('/api/days_of_week/<int:id>', methods=['DELETE'])
def delete_day_of_week(id):
    day_of_week = DayOfWeek.query.get(id)
    if not day_of_week:
        abort(404)
    db.session.delete(day_of_week)
    db.session.commit()
    return jsonify({'message': 'Day of week deleted successfully'}), 200

@app.route('/api/coaches', methods=['GET', 'POST'])
def handle_coaches():
    if request.method == 'GET':
        coaches = Coach.query.all()
        coaches_list = [{'id': coach.id, 'name': coach.name, 'photo': coach.photo, 'description': coach.description} for coach in coaches]
        return jsonify(coaches_list), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_coach = Coach(name=data['name'], photo=data.get('photo'), description=data.get('description'))
        db.session.add(new_coach)
        db.session.commit()
        return jsonify({'id': new_coach.id, 'name': new_coach.name}), 201

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
    if request.method == 'GET':
        subscriptions = Subscription.query.all()
        subscriptions_list = [{'id': sub.id, 'name': sub.name, 'price': sub.price} for sub in subscriptions]
        return jsonify(subscriptions_list), 200

    elif request.method == 'POST':
        data = request.get_json()
        new_subscription = Subscription(name=data['name'], price=data['price'])
        db.session.add(new_subscription)
        db.session.commit()
        return jsonify({'id': new_subscription.id, 'name': new_subscription.name, 'price': new_subscription.price}), 201

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
    if request.method == 'GET':
        workouts = Workout.query.all()
        workouts_list = [{
            'id': workout.id,
            'exercise_type_id': workout.exercise_type_id,
            'day_of_week_id': workout.day_of_week_id,
            'coach_id': workout.coach_id,
            'date': workout.date.isoformat(),
            'time': workout.time.isoformat()
        } for workout in workouts]
        return jsonify(workouts_list), 200

    elif request.method == 'POST':
        data = request.get_json()

        # Преобразуем строку даты в объект date
        date_value = datetime.strptime(data['date'], '%Y-%m-%d').date()

        # Преобразуем строку времени в объект time
        time_value = datetime.strptime(data['time'], '%H:%M:%S').time()

        # Создаем новый объект Workout
        new_workout = Workout(
            exercise_type_id=data['exercise_type_id'],
            day_of_week_id=data['day_of_week_id'],
            coach_id=data['coach_id'],
            date=date_value,  # Используем преобразованный объект date
            time=time_value   # Используем преобразованный объект time
        )

        db.session.add(new_workout)
        db.session.commit()

        return jsonify({
            'id': new_workout.id,
            'exercise_type_id': new_workout.exercise_type_id,
            'day_of_week_id': new_workout.day_of_week_id,
            'coach_id': new_workout.coach_id,
            'date': new_workout.date.isoformat(),
            'time': new_workout.time.isoformat()
        }), 201