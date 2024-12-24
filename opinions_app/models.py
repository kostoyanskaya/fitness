from datetime import datetime

from opinions_app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    telephone = db.Column(db.Integer)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class ExerciseType(db.Model):
    __tablename__ = 'exercise_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    workouts = db.relationship('Workout', backref='exercise_type', lazy=True)

    def __repr__(self):
        return f"ExerciseType('{self.name}')"

class DayOfWeek(db.Model):
    __tablename__ = 'day_of_week'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    workouts = db.relationship('Workout', backref='day_of_week', lazy=True)

    def __repr__(self):
        return f"DayOfWeek('{self.name}')"

class Coach(db.Model):
    __tablename__ = 'coach'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(255), nullable=True)  # Путь к фото тренера
    description = db.Column(db.Text, nullable=True)  # Описание тренера
    workouts = db.relationship('Workout', backref='coach', lazy=True)

    def __repr__(self):
        return f"Coach('{self.name}')"

class Workout(db.Model):
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True)
    exercise_type_id = db.Column(db.Integer, db.ForeignKey('exercise_type.id'), nullable=False)
    day_of_week_id = db.Column(db.Integer, db.ForeignKey('day_of_week.id'), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return (f"Workout(exercise_type='{self.exercise_type.name}', "
                f"day_of_week='{self.day_of_week.name}', "
                f"coach='{self.coach.name}', "
                f"date='{self.date}', time='{self.time}')")

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    date_booked = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='bookings')
    workout = db.relationship('Workout', backref='bookings')

    def __repr__(self):
        return f"Booking(user_id='{self.user_id}', workout_id='{self.workout_id}', date_booked='{self.date_booked}')"
    

class PersonalTraining(db.Model):
    __tablename__ = 'personaltraining'
    id = db.Column(db.Integer, primary_key=True)
    exercise_type_id = db.Column(db.Integer, db.ForeignKey('exercise_type.id'), nullable=False)
    day_of_week_id = db.Column(db.Integer, db.ForeignKey('day_of_week.id'), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    coach = db.relationship('Coach', backref='bookings')
    exercise_type = db.relationship('ExerciseType')
    day_of_week = db.relationship('DayOfWeek')

    def __repr__(self):
        return f"PersonalTraining('{self.id}', '{self.date}', '{self.time}')"