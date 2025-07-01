# app.py
"""
Main Flask application for the MoviWeb App.
Handles routing, OMDb API integration, and interacts with the DataManager.
"""

from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, User, Movie

app = Flask(__name__)

# --- SQLAlchemy Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- DataManager Initialization ---
data_manager = DataManager()

# --- Database Table Creation ---
# Creates database tables if they don't exist within the application context.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    """
    Renders the home page of the application, displaying a list of all
    registered users and a form for adding new users.
    """
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """
    Handles the form submission for adding a new user.
    Retrieves the user name from the form and creates a new user in the database.
    Redirects back to the home page after successful creation.
    """
    user_name = request.form.get('user_name')
    if user_name:
        data_manager.create_user(user_name)
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_user_movies(user_id: int):
    """
    Displays the list of favorite movies for a specific user.
    Includes a form to add new movies to this user's list.

    Args:
        user_id (int): The ID of the user whose movies to display.
    """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        return redirect(url_for('home')) # Redirect if user not found

    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', user=user, movies=movies)


# Main entry point for running the Flask application.
if __name__ == '__main__':
    app.run(debug=True)