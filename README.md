# Project: Fitnesite
"Fitnesite" is a modern web resource dedicated to a gym, where an active lifestyle is the center of attention. On the website, users can easily find complete information about our fitness center: from the training schedule to photos.
Here you will find profiles of our trainers, who are ready to share their knowledge and experience, as well as various training programs suitable for people with different levels of preparation. Viewing prices for memberships and individual classes will help users make an informed choice.

After registering on "Fitnesite," users will get access to a personal account, where they can sign up for personal or group training sessions, as well as manage their schedule. All scheduled classes will be visible in the personal profile, ensuring maximum flexibility. If necessary, users can easily cancel any class, while maintaining full control over their time.

With "Fitnesite," you will be closer to your fitness goals, getting the opportunity to work out at a convenient time for you in the company of professional trainers and like-minded people!

The site is currently being updated and improved.

### Main features:
Main features:

- Complete information about the fitness center, including the training schedule and photos of the gym.

- Trainer profiles with a description of their experience and methods.

- Information on membership and individual class prices for an informed choice.

- User registration to gain access to the personal account.

- Ability to sign up for personal and group training sessions.

- Managing the training schedule with the ability to view scheduled classes.

- Function to cancel scheduled training sessions to ensure flexibility in planning.


### The project mainly uses the following technologies and libraries:

Flask (==2.0.2): A lightweight Python web framework that provides simplicity and flexibility in web application development. Used as the main framework for creating the server side of the application.

Flask-SQLAlchemy (==2.5.1): An extension for Flask that helps integrate ORM (Object Relational Mapping) into Python applications, simplifying work with databases.

Flask-Migrate (==3.1.0): An add-on for Flask that simplifies database migration, allowing you to manage database schema changes using Alembic.

Alembic (==1.14.0): A tool for managing database schema migrations in SQLAlchemy. Allows you to create and change database structures in a controlled and consistent order.

PostgreSQL: A relational database management system (DBMS), which is used in the project for reliable storage and management of user data, training sessions, and other information.
Flask-Login (==0.6.3): A library for managing user sessions, providing login and logout functionality for application users.

Flask-WTF (==1.0.0): An extension for Flask, providing integration with libraries for form processing, including protection against CSRF attacks.

Flask-Admin (==1.5.8): A convenient interface for database administration, allowing developers to quickly create control panels for managing application content.

Flask-Bcrypt (==1.0.1): A library for password hashing, providing protection for users' confidential information.

psycopg2-binary (==2.9.10): A PostgreSQL adapter for Python, which allows interaction with the PostgreSQL database.

marshmallow (==3.23.2): A library for object serialization and deserialization, allowing easy data exchange between the application and the client.

WTForms (==3.0.0): A library for working with forms, which simplifies the creation and validation of forms in web applications.

requests (==2.32.3): A library for convenient execution of HTTP requests, which simplifies interaction with external APIs.

Jinja2 (==3.0.3): A template engine built into Flask, allows you to easily generate HTML using templates.

bcrypt (==4.2.1): A library for password hashing using the Bcrypt algorithm, providing a high degree of security.

python-dotenv (==0.19.2): A package for loading configuration variables from a .env file, which helps manage application settings.

Werkzeug (==2.0.2): A library for creating web applications and debugging, which is the foundation for Flask and provides low-level tools for working with WSGI.



## Installing the project on a remote server:

1. Cloning the repository
```
git@github.com:kostoyanskaya/fitness.git
```

2. Navigate to the fitness directory

```
cd fitness
```

3. Creating a virtual environment

```
python -m venv venv
```

4. Activating the virtual environment

```
source venv/Scripts/activate
```

5. Update pip

```
python -m pip install --upgrade pip
```

6. Installing dependencies

```
pip install -r requirements.txt
```

7. You need to create a .env file

8. Fill it out according to the example

```
FLASK_APP=fitness_app
FLASK_DEBUG=1
DATABASE_URI=postgresql://username:password@localhost:5432/database_name
SECRET_KEY=YOUR_SECRET_KEY
```

9. Run the commands:
```
flask db init
flask db migrate
flask db upgrade

```

10. Load objects into the database:

```
flask import-all data.json
```
10. Run the site:

```
flask run
```

## Example request:


```
http://127.0.0.1:5000/api/register
```
body:
```
{
    "fullname": "name",
    "email": "user@example.com",
    "password": "password1",
    "confirmpassword": "password1"
}
```

## Author
#### [_Victoria_](https://github.com/kostoyanskaya/)
