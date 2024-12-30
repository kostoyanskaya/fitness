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
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
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

        new_coach = Coach(name=data['name'], photo=photo_path, description=data.get('description'))
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
        date_value = datetime.strptime(data['date'], '%Y-%m-%d').date()
        time_value = datetime.strptime(data['time'], '%H:%M:%S').time()
        new_workout = Workout(
            exercise_type_id=data['exercise_type_id'],
            day_of_week_id=data['day_of_week_id'],
            coach_id=data['coach_id'],
            date=date_value,
            time=time_value
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


@app.route('/api/bookings', methods=['POST'])
def book_workouts():
    data = request.get_json()
    user_id = data.get('user_id')
    workout_id = data['workout_id']

    new_booking = Booking(user_id=user_id, workout_id=workout_id)
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({
        'message': 'Successfully booked workout.',
        'booking_id': new_booking.id
    }), 201


@app.route('/api/personal_trainings', methods=['POST'])
def book_personal_training():
    data = request.get_json()
    user_id = current_user.id
    print(user_id) 
    coach_id = int(data.get('coach_id'))
    date_str = data.get('date')
    time_str = data.get('time')

    date_value = datetime.strptime(date_str, '%Y-%m-%d').date()
    time_value = datetime.strptime(time_str, '%H:%M').time()
    day_of_week_id = (date_value.weekday() + 1) % 7 + 1

    coach = Coach.query.get(coach_id)
    if not coach or not coach.workouts:
        return jsonify({'error': 'Тренер не найден или у него нет доступных типов тренировок.'}), 404

    new_training = PersonalTraining(
        user_id=user_id,
        coach_id=coach_id,
        day_of_week_id=day_of_week_id,
        date=date_value,
        time=time_value
    )
    print(new_training)

    db.session.add(new_training)
    db.session.commit()

    return jsonify({
        'message': 'Успешно записано на персональную тренировку.',
        'personal_training_id': new_training.id
    }), 201


@app.route('/api/user/trainings', methods=['GET'])
def get_user_trainings():
    if current_user.is_authenticated:
        print(f"Текущий пользователь: {current_user.id}")
        bookings = Booking.query.filter_by(user_id=current_user.id).all()
        workouts = []

        for booking in bookings:
            workout = Workout.query.get(booking.workout_id)
            exercise_type = ExerciseType.query.get(workout.exercise_type_id)
            coach = Coach.query.get(workout.coach_id)
            workouts.append({
                'id': workout.id,
                'date': workout.date.strftime('%Y-%m-%d'),
                'time': workout.time.strftime('%H:%M'),
                'exercise': exercise_type.name if exercise_type else 'Unknown',
                'coach': coach.name if coach else 'Unknown'
            })

        personal_workouts = PersonalTraining.query.filter_by(user_id=current_user.id).all()
        print(f"Персональные тренировки для пользователя {current_user.id}: {personal_workouts}")
        personal_workouts_data = []
        
        for personal_workout in personal_workouts:
            coach = Coach.query.get(personal_workout.coach_id)
            personal_workouts_data.append({
                'id': personal_workout.id,
                'date': personal_workout.date.strftime('%Y-%m-%d'),
                'time': personal_workout.time.strftime('%H:%M'),
                'exercise': 'Персональная тренировка',
                'coach': coach.name if coach else 'Unknown'
            })

        return jsonify({
            'workouts': workouts,
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
