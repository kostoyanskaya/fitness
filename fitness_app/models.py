from datetime import datetime

from flask_login import UserMixin

from fitness_app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    telephone = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class ExerciseType(db.Model):
    __tablename__ = 'exercise_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    workouts = db.relationship(
        'Workout',
        backref='exercise_type',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"ExerciseType('{self.name}')"


class DayOfWeek(db.Model):
    __tablename__ = 'day_of_week'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(12), unique=True, nullable=False)
    workouts = db.relationship(
        'Workout', backref='day_of_week', cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"DayOfWeek('{self.name}')"


class Coach(db.Model):
    __tablename__ = 'coach'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(400), nullable=True)
    description = db.Column(db.Text, nullable=True)
    workouts = db.relationship(
        'Workout', backref='coach', lazy=True, cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"Coach('{self.name}')"


class Workout(db.Model):
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True)
    exercise_type_id = db.Column(
        db.Integer,
        db.ForeignKey('exercise_type.id'),
        nullable=False
    )
    day_of_week_id = db.Column(
        db.Integer,
        db.ForeignKey('day_of_week.id'),
        nullable=False
    )
    coach_id = db.Column(
        db.Integer,
        db.ForeignKey('coach.id'),
        nullable=False
    )
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"<Workout {self.id}>"


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    workout_id = db.Column(
        db.Integer,
        db.ForeignKey('workout.id'),
        nullable=False
    )
    date_booked = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        'User',
        backref=db.backref('bookings', cascade='all, delete-orphan')
    )
    workout = db.relationship(
        'Workout',
        backref=db.backref('bookings', cascade='all, delete-orphan')
    )

    def __repr__(self):
        return (f"Booking(user_id='{self.user_id}', "
                f"workout_id='{self.workout_id}', "
                f"date_booked='{self.date_booked}')")


class PersonalTraining(db.Model):
    __tablename__ = 'personal_training'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
    )
    day_of_week_id = db.Column(
        db.Integer,
        db.ForeignKey('day_of_week.id', ondelete='CASCADE'),
        nullable=False
    )
    coach_id = db.Column(
        db.Integer,
        db.ForeignKey('coach.id', ondelete='CASCADE'),
        nullable=False
    )
    workout_type = db.Column(
        db.String,
        default="Персональная тренировка"
    )

    coach = db.relationship(
        'Coach',
        backref=db.backref('personaltrainings', cascade='all, delete-orphan')
    )
    day_of_week = db.relationship(
        'DayOfWeek',
        backref=db.backref('personaltrainings', cascade='all, delete-orphan')
    )
    user = db.relationship(
        'User',
        backref=db.backref('personal_trainings', cascade='all, delete-orphan')
    )

    def __repr__(self):
        return (
            f"<PersonalTraining('{self.date}', '{self.time}', "
            f"'User ID: {self.user_id}')>"
        )


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Price {self.name}>'
