# app.py
"""
Main Flask application for the MoviWeb App.
Handles routing, OMDb API integration, and interacts with the DataManager.
"""

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
from models import db, User, Movie

app = Flask(__name__)

# --- SQLAlchemy Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviweb.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppress warning

db.init_app(app) # Initialize SQLAlchemy with the Flask app

# --- DataManager Initialization ---
data_manager = DataManager()

# --- Database Table Creation (run once) ---
# This block ensures tables are created when the app context is pushed.
# It's good for initial setup and development.



@app.route('/')
def home():
    """
    Renders the home page, displaying a list of all registered users
    and a form for adding new users.
    """
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """
    Handles the form submission for adding a new user.
    Redirects back to the home page after creation.
    """
    user_name = request.form.get('user_name')
    if user_name:
        data_manager.create_user(user_name)
    return redirect(url_for('home')) # Redirect back to the home page


@app.route('/users') # This route needs to be changed or removed later as / is the user list
def list_users():
    """
    DEPRECATED: This route was for temporarily displaying users as a string.
    The / route now handles user display.
    """
    users = data_manager.get_users()
    return str(users)

if __name__ == '__main__':
    app.run(debug=True)