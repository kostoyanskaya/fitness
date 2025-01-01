from marshmallow import Schema, fields, post_load
from .models import Subscription, Workout, Booking, PersonalTraining


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()


class ExerciseTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class DayOfWeekSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class CoachSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    photo = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)


class SubscriptionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

    @post_load
    def create_subscription(self, data, **kwargs):
        return Subscription(**data)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    exercise_type_id = fields.Int(required=True)
    day_of_week_id = fields.Int(required=True)
    coach_id = fields.Int(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)

    @post_load
    def create_workout(self, data, **kwargs):
        return Workout(**data)

class BookingSchema(Schema):
    user_id = fields.Int(required=True)
    workout_id = fields.Int(required=True)

    @post_load
    def create_booking(self, data, **kwargs):
        return Booking(**data)

class PersonalTrainingSchema(Schema):
    coach_id = fields.Int(required=True)
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    day_of_week_id = fields.Int(required=True)
    user_id = fields.Int(required=True)

    @post_load
    def create_personal_training(self, data, **kwargs):
        return PersonalTraining(**data)