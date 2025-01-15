from flask import redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import current_user

from fitness_app import app
from .utils import search_in_templates

bcrypt = Bcrypt(app)


@app.route('/register')
def register():
    return render_template('login.html')


@app.route('/home')
def index_view():
    """Главная страница."""
    return render_template('home.html')


@app.route('/me')
def me_view():
    if current_user.is_authenticated:
        return render_template('person.html')
    return redirect(url_for('register'))


@app.route('/booking')
def book_workout():
    return render_template('book_workout.html')


@app.route('/teacher')
def teacher_view():
    return render_template(
        'my_teacher.html', static_url=url_for('static', filename='')
    )


@app.route('/contacts')
def information_view():
    """Контакты."""
    return render_template('contacts.html')


@app.route('/price')
def price_view():
    """Ценообразование."""
    return render_template('cost.html')


@app.route('/search')
def search():
    query = request.args.get('q')
    results = search_in_templates(query)
    if results:
        return redirect(url_for('redirect_to_template', filename=results[0]))
    return render_template('search_results.html', results=results, query=query)


@app.route('/redirect_to/<filename>')
def redirect_to_template(filename):
    return render_template(filename, static_url=url_for('static', filename=''))
