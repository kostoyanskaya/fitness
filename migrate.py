from task_app import create_app
from task_app.extensions import db, migrate
from flask_migrate import (
    upgrade,
    downgrade,
    migrate as flask_migrate,
    init as flask_init
)

app = create_app()


migrate.init_app(app, db)

if __name__ == '__main__':
    import sys
    command = sys.argv[1] if len(sys.argv) > 1 else None

    if command == 'init':
        print("Инициализация миграций...")
        with app.app_context():
            flask_init()
    elif command == 'migrate':
        message = sys.argv[2] if len(sys.argv) > 2 else "Automatic migration"
        print(f"Создание миграции: {message}")
        with app.app_context():
            flask_migrate(message=message)
    elif command == 'upgrade':
        print("Применение миграций...")
        with app.app_context():
            upgrade()
    elif command == 'downgrade':
        print("Откат миграций...")
        with app.app_context():
            downgrade()
    else:
        print("Использование: python migrate.py")
