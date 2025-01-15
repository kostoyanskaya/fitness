import os

from flask import abort, jsonify, request
from flask_bcrypt import Bcrypt
from flask_login import (
    current_user, LoginManager, login_required,
    login_user, logout_user
)
import requests
from werkzeug.utils import secure_filename

from opinions_app import app
from .decorators import role_required, role_required_for_methods
from .models import (
    Booking, Coach, DayOfWeek, ExerciseType,
    PersonalTraining, Price, User, Workout, db
)
from .schemas import (
    BookingSchema, CoachSchema, DayOfWeekSchema,
    ExerciseTypeSchema, PersonalTrainingSchema,
    PriceSchema, UserSchema, WorkoutSchema,
    WorkoutSchemaForUsers
)
from .validators import validate_registration_data
from marshmallow import ValidationError

login_manager = LoginManager(app)
login_manager.login_view = 'register'

bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/api/users', methods=['GET'])
@role_required('admin')
def get_users():
    users = User.query.all()
    if not users:
        abort(404)
    user_schema = UserSchema(many=True)
    users_list = user_schema.dump(users)
    return jsonify(users_list), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user)), 200 


@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify('Выход выполнен успешно!'), 200


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    if current_user.id != user.id:
        return jsonify('Нет доступа'), 403
    db.session.delete(user)
    db.session.commit()
    return jsonify('Пользователь успешно удален'), 200


@app.route('/api/exercise_types', methods=['GET', 'POST'])
@role_required_for_methods()
def handle_exercise_types():
    exercise_type_schema = ExerciseTypeSchema()

    if request.method == 'GET':
        exercise_types = ExerciseType.query.all()
        if not exercise_types:
            abort(404)
        exercise_types_list = exercise_type_schema.dump(
            exercise_types,
            many=True
        )
        return jsonify(exercise_types_list), 200

    data = request.get_json()
    new_exercise_type = exercise_type_schema.load(data)
    exercise_type = ExerciseType(**new_exercise_type)
    db.session.add(exercise_type)
    db.session.commit()
    response = exercise_type_schema.dump(exercise_type)
    return jsonify(response), 201


@app.route('/api/exercise_types/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_exercise_type(id):
    exercise_type = ExerciseType.query.get(id)
    if not exercise_type:
        abort(404)
    db.session.delete(exercise_type)
    db.session.commit()
    return jsonify('Тип упражнения успешно удален'), 200


@app.route('/api/days_of_week', methods=['GET', 'POST'])
@role_required_for_methods()
def handle_days_of_week():
    day_of_week_schema = DayOfWeekSchema()

    if request.method == 'GET':
        days_of_week = DayOfWeek.query.all()
        if not days_of_week:
            abort(404)
        days_list = day_of_week_schema.dump(days_of_week, many=True)
        return jsonify(days_list), 200

    data = request.get_json()
    new_day_of_week = day_of_week_schema.load(data)
    day_of_week = DayOfWeek(**new_day_of_week)
    db.session.add(day_of_week)
    db.session.commit()
    return jsonify(day_of_week_schema.dump(day_of_week)), 201


@app.route('/api/days_of_week/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_day_of_week(id):
    day_of_week = DayOfWeek.query.get(id)
    if not day_of_week:
        abort(404)
    db.session.delete(day_of_week)
    db.session.commit()
    return jsonify('День недели успешно удален'), 200


@app.route('/api/coaches', methods=['GET', 'POST'])
@role_required_for_methods()
def handle_coaches():
    coach_schema = CoachSchema()
    if request.method == 'GET':
        coaches = Coach.query.all()
        coaches_list = coach_schema.dump(coaches, many=True)
        return jsonify(coaches_list), 200
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
        except requests.exceptions.RequestException:
            return jsonify('Не удалось загрузить изображение'), 400
    new_coach_data = coach_schema.load(data)
    new_coach = Coach(
        name=new_coach_data['name'],
        description=new_coach_data.get('description'),
        photo=photo_path
    )
    db.session.add(new_coach)
    db.session.commit()

    return jsonify(coach_schema.dump(new_coach)), 201


@app.route('/api/coaches/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_coach(id):
    coach = Coach.query.get(id)
    if not coach:
        abort(404)
    db.session.delete(coach)
    db.session.commit()
    return jsonify('Тренер удален успешно'), 200


@app.route('/api/prices', methods=['GET', 'POST'])
@role_required_for_methods()
def handle_prices():
    price_schema = PriceSchema()

    if request.method == 'GET':
        prices = Price.query.all()
        if not prices:
            abort(404, description='Цены не найдены')
        return jsonify(price_schema.dump(prices, many=True)), 200

    data = request.get_json()
    new_price = price_schema.load(data)
    db.session.add(new_price)
    db.session.commit()
    return price_schema.dump(new_price), 201


@app.route('/api/prices/<int:id>', methods=['DELETE'])
@role_required('admin')
def delete_price(id):
    price = Price.query.get(id)
    if not price:
        abort(404, description='Цена не найдена')
    db.session.delete(price)
    db.session.commit()
    return jsonify('Цена успешно удалена'), 200


@app.route('/api/workouts', methods=['GET', 'POST'])
@role_required_for_methods()
def handle_workouts():
    workout_schema = WorkoutSchema()

    if request.method == 'GET':
        workout_schema_get = WorkoutSchemaForUsers()
        workouts = Workout.query.all()
        if not workouts:
            abort(404, description='Нет тренировок')
        return jsonify(workout_schema_get.dump(workouts, many=True)), 200

    data = request.get_json()
    new_workout = workout_schema.load(data)
    db.session.add(new_workout)
    db.session.commit()
    return workout_schema.dump(new_workout), 201


@app.route('/api/bookings', methods=['POST'])
def book_workouts():
    if current_user.is_authenticated:
        booking_schema = BookingSchema()
        data = request.get_json()
        user_id = current_user.id
        new_booking = booking_schema.load({**data, 'user_id': user_id})
        existing_booking = Booking.query.filter_by(
            user_id=user_id,
            workout_id=new_booking.workout_id
        ).first()
        if existing_booking:
            return jsonify('Вы уже записаны на эту тренировку.'), 400
        db.session.add(new_booking)
        db.session.commit()
        return jsonify('Успешно записаны на тренировку.'), 201
    return jsonify('Войдите или зарегистрируйтесь для записи'), 401


@app.route('/api/personal_trainings', methods=['POST'])
def book_personal_training():
    if current_user.is_authenticated:
        personal_training_schema = PersonalTrainingSchema()
        data = request.get_json()
        data['user_id'] = current_user.id
        data['workout_type'] = "Персональная тренировка"
        coach = Coach.query.get(data['coach_id'])
        if not coach:
            return jsonify('Тренер не найден.'), 404
        new_training = personal_training_schema.load(data)
        db.session.add(new_training)
        db.session.commit()
        return jsonify('Успешно записаны на персональную тренировку.'), 201
    return jsonify('Войдите или зарегистрируйтесь для записи'), 401


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
        personal_workouts = PersonalTraining.query.filter_by(
            user_id=current_user.id
        ).all()
        personal_training_schema = PersonalTrainingSchema(many=True)
        personal_workouts_data = personal_training_schema.dump(
            personal_workouts
        )
        return jsonify({
            'workouts': workouts_data,
            'personal_workouts': personal_workouts_data
        }), 200
    return jsonify('Нет доступа'), 401


@app.route('/api/bookings/<int:workout_id>', methods=['DELETE'])
@login_required
def cancel_booking(workout_id):
    booking = Booking.query.filter_by(
        workout_id=workout_id, user_id=current_user.id
    ).first()
    if not booking:
        return jsonify('Тренировка не найдена.')
    db.session.delete(booking)
    db.session.commit()

    return jsonify('Тренировка отменена.'), 200


@app.route(
        '/api/cancel_personal_booking/<int:personal_booking_id>',
        methods=['DELETE']
    )
def cancel_personal_booking(personal_booking_id):
    if current_user.is_authenticated:
        personal_booking = PersonalTraining.query.filter_by(
            id=personal_booking_id, user_id=current_user.id
        ).first()
        if personal_booking:
            db.session.delete(personal_booking)
            db.session.commit()
            return jsonify('Тренировка отменена.'), 200
        return jsonify('Персональная тренировка не найдена.'), 404
    return jsonify('Нет доступа'), 401


@app.route('/api/create_admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    fullname = data.get('username')
    password = data.get('password')
    email = data.get('email')
    confirmpassword = data.get('confirmpassword')
    validation_error = validate_registration_data(
        fullname, email, password, confirmpassword
    )
    if validation_error:
        return validation_error
    new_admin = User(
        username=fullname,
        email=email,
        password=bcrypt.generate_password_hash(password).decode('utf-8'),
        is_admin=True
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify('Администратор успешно создан!'), 201


@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')
    confirmpassword = data.get('confirmpassword')
    validation_error = validate_registration_data(
        fullname, email, password, confirmpassword
    )
    if validation_error:
        return jsonify({'message': validation_error[0]}), validation_error[1]
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=fullname, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify('Ваш аккаунт был создан!'), 201


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify('Вход успешен!'), 200
    return jsonify('Вход не удался. Пожалуйста, проверьте имя и пароль!'), 401
