# app.py
"""
Main Flask application for the MoviWeb App.
Handles routing, OMDb API integration, and interacts with the DataManager.
"""

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

from flask import Flask, render_template # Add render_template here
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
    Renders the home page, which will eventually list all users and
    provide a form to add new users.
    """
    return render_template('index.html') # Render the index.html template


@app.route('/users')
def list_users():
    """
    Retrieves and temporarily displays a list of all registered users.
    This will be updated to render a proper HTML template later.
    """
    users = data_manager.get_users()
    return str(users)

if __name__ == '__main__':
    app.run(debug=True)