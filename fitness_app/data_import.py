import os
import json
import click
from flask import Flask
from fitness_app import app
from .decorators import role_required, role_required_for_methods
from .models import (
    Booking, Coach, DayOfWeek, ExerciseType,
    PersonalTraining, Price, User, Workout, db
)

class BaseImportCommand:
    help = 'Импорт данных из JSON файла'

    def import_data(self, model_class, data):
        objects = [model_class(**item) for item in data]
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
        print(f"Импортировано {count_users} пользователей.")
        total_imported += count_users
    
    if "exercise_types" in data:
        count_exercise_types = command.import_data(ExerciseType, data["exercise_types"])
        print(f"Импортировано {count_exercise_types} типов упражнений.")
        total_imported += count_exercise_types
    
    if "days_of_week" in data:
        count_days_of_week = command.import_data(DayOfWeek, data["days_of_week"])
        print(f"Импортировано {count_days_of_week} дней недели.")
        total_imported += count_days_of_week
    
    print(f"Всего импортировано {total_imported} записей.")