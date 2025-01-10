from marshmallow import Schema, fields, post_load, post_dump
from .models import Price, Workout, Booking, PersonalTraining
from datetime import time


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
    
class WorkoutSchemaForUsers(Schema):
    id = fields.Int(dump_only=True)
    exercise_type = fields.Str(attribute="exercise_type.name")
    day_of_week = fields.Str(attribute="day_of_week.name")
    coach = fields.Str(attribute="coach.name")
    date = fields.Date(required=True)
    time = fields.Time(required=True)

    @post_load
    def create_workout(self, data, **kwargs):
        return Workout(**data)


class CoachSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    photo = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    workouts = fields.Nested(WorkoutSchemaForUsers, many=True, allow_none=True)

    @post_dump
    def add_default_workout_type(self, data, **kwargs):
        if not data.get('workouts'):
            data['workouts'] = [{'exercise_type': 'Персональный тренер'}] 
        return data


class PriceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

    @post_load
    def create_price(self, data, **kwargs):
        return Price(**data)



class WorkoutSchemaForUsers(Schema):
    id = fields.Int(dump_only=True)
    exercise_type = fields.Str(attribute="exercise_type.name")
    day_of_week = fields.Str(attribute="day_of_week.name")
    coach = fields.Str(attribute="coach.name")
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
    id = fields.Int(dump_only=True)
    coach_id = fields.Int(required=False)
    coach_name = fields.String(required=False, attribute='coach.name')
    date = fields.Date(required=True)
    time = fields.Time(required=True)
    day_of_week_name = fields.String(required=False, attribute='day_of_week.name')
    user_id = fields.Int(required=True)
    workout_type = fields.String(required=True, default="Персональная тренировка")

    @post_load
    def create_personal_training(self, data, **kwargs):
        date_value = data.get('date')
        if date_value:
            day_of_week = date_value.weekday()
            data['day_of_week_id'] = day_of_week + 1
        return PersonalTraining(**data)