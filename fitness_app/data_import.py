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
import os
import requests
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_bcrypt import Bcrypt

# Инициализация Bcrypt
bcrypt = Bcrypt()
#flask import-all data.json

class BaseImportCommand:
    help = 'Импорт данных из JSON файла'

    def import_data(self, model_class, data):
        objects = []
        for item in data:
            if 'date' in item:
                item['date'] = datetime.strptime(item['date'], '%Y-%m-%d').date()
            if 'time' in item:
                item['time'] = datetime.strptime(item['time'], '%H:%M:%S').time()
            if 'password' in item and model_class == User:  # Хешируем пароль, если это пользователь
                item['password'] = bcrypt.generate_password_hash(item['password']).decode('utf-8')
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

    if "prices" in data:  # Новый блок для Price
        count_prices = command.import_data(Price, data["prices"])
        print(f"Импортировано {count_prices} цен.")
        total_imported += count_prices
    
    if "coaches" in data:  # Новый блок для Coach
        count_coaches = command.import_data(Coach, data["coaches"])
        print(f"Импортировано {count_coaches} тренеров.")
        total_imported += count_coaches
    
    if "workouts" in data:
        count_workouts = command.import_data(Workout, data["workouts"])
        print(f"Импортировано {count_workouts} тренировок.")
        total_imported += count_workouts
    
    print(f"Всего импортировано {total_imported} записей.")