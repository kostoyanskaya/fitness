from datetime import datetime
import json

import click
from flask_bcrypt import Bcrypt

from fitness_app import app
from .models import (
    Coach, DayOfWeek, ExerciseType,
    Price, User, Workout, db
)

bcrypt = Bcrypt()


class BaseImportCommand:
    help = 'Импорт данных из JSON файла'

    def import_data(self, model_class, data):
        objects = []
        for item in data:
            if 'date' in item:
                date_str = item['date']
                item['date'] = datetime.strptime(date_str, '%Y-%m-%d').date()

            if 'time' in item:
                time_str = item['time']
                item['time'] = datetime.strptime(time_str, '%H:%M:%S').time()

            if 'password' in item and model_class == User:
                password = item['password']
                hashed_password = bcrypt.generate_password_hash(password)
                item['password'] = hashed_password.decode('utf-8')

            objects.append(model_class(**item))
        db.session.bulk_save_objects(objects)
        db.session.commit()
        return len(objects)


@app.cli.command("import-all")
@click.argument("json_file")
def import_all(json_file):
    command = BaseImportCommand()
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    total_imported = 0

    if "users" in data:
        count_users = command.import_data(User, data["users"])
        total_imported += count_users

    if "exercise_types" in data:
        count_exercise_types = command.import_data(
            ExerciseType, data["exercise_types"]
        )
        total_imported += count_exercise_types

    if "days_of_week" in data:
        count_days_of_week = command.import_data(
            DayOfWeek, data["days_of_week"]
        )
        total_imported += count_days_of_week

    if "prices" in data:
        count_prices = command.import_data(Price, data["prices"])
        total_imported += count_prices

    if "coaches" in data:
        count_coaches = command.import_data(Coach, data["coaches"])
        total_imported += count_coaches

    if "workouts" in data:
        count_workouts = command.import_data(Workout, data["workouts"])
        total_imported += count_workouts

    print(f"Всего импортировано {total_imported} записей.")
