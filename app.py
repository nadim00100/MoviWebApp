# app.py
"""
Main Flask application for the MoviWeb App.
Handles routing, OMDb API integration, and interacts with the DataManager.
"""

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

from flask import Flask
from data_manager import DataManager
from models import db, User, Movie # Import db, User, and Movie models

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
    Renders the home page of the application.
    Currently, displays a welcome message.
    """
    return "Welcome to MoviWeb App!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)