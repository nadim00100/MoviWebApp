# app.py
"""
Main Flask application for the MoviWeb App.
Handles routing, OMDb API integration, and interacts with the DataManager.
"""

from dotenv import load_dotenv
import os
import requests # Added for OMDb API calls

load_dotenv()

from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import db, User, Movie

app = Flask(__name__)
# Add a secret key for session management (required for flash messages)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_very_secret_fallback_key_for_dev') # GET FROM .env or use fallback

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
        flash(f"User '{user_name}' created successfully!", 'success') # Flash message
    else:
        flash("User name cannot be empty!", 'error') # Flash message
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def list_user_movies(user_id: int):
    """
    Displays the list of favorite movies for a specific user via GET request.
    Handles adding a new movie to the user's list via POST request,
    including fetching movie details from the OMDb API.

    Args:
        user_id (int): The ID of the user.
    """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        flash("User not found!", 'error') # Flash message
        return redirect(url_for('home'))

    if request.method == 'POST':
        movie_title = request.form.get('movie_name')
        if movie_title:
            omdb_api_key = os.getenv('OMDB_API_KEY')
            if not omdb_api_key:
                print("Error: OMDb API Key not found in .env. Please set it up.")
                flash("OMDb API Key not configured. Cannot add movie.", 'error') # Flash message
                return redirect(url_for('list_user_movies', user_id=user.id))

            omdb_url = f"http://www.omdbapi.com/?t={movie_title}&apikey={omdb_api_key}"
            try:
                response = requests.get(omdb_url)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
                movie_data = response.json()

                if movie_data and movie_data.get('Response') == 'True':
                    # Extract relevant data, handling potential missing fields
                    name = movie_data.get('Title')
                    director = movie_data.get('Director')
                    # Ensure 'Year' is an integer, or None if not available/valid
                    year = int(movie_data.get('Year', 0)) if movie_data.get('Year') and movie_data.get('Year').isdigit() else None
                    poster_url = movie_data.get('Poster')

                    # Create Movie object and add to DB
                    new_movie = Movie(
                        name=name,
                        director=director,
                        year=year,
                        poster_url=poster_url,
                        user_id=user.id
                    )
                    data_manager.add_movie(new_movie)
                    flash(f"Movie '{name}' added successfully!", 'success') # Flash message
                else:
                    error_message = movie_data.get('Error', 'Unknown Error')
                    print(f"Movie '{movie_title}' not found on OMDb or API error: {error_message}")
                    flash(f"Could not add movie '{movie_title}': {error_message}", 'warning') # Flash message
            except requests.exceptions.RequestException as e:
                print(f"Error fetching movie from OMDb: {e}")
                flash(f"Error connecting to OMDb. Could not add movie '{movie_title}'.", 'error') # Flash message
        else:
            flash("Movie title cannot be empty!", 'error') # Flash message
        return redirect(url_for('list_user_movies', user_id=user.id))

    # This block executes for GET requests: display the movies
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/edit', methods=['GET'])
def edit_movie(user_id: int, movie_id: int):
    """
    Displays a form to edit the details of a specific movie.

    Args:
        user_id (int): The ID of the user who owns the movie.
        movie_id (int): The ID of the movie to be edited.
    """
    user = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_by_id(movie_id)

    if not user or not movie or movie.user_id != user_id:
        flash("Movie or user not found, or movie doesn't belong to user.", 'error') # Flash message
        return redirect(url_for('home'))

    return render_template('edit_movie.html', user=user, movie=movie)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id: int, movie_id: int):
    """
    Handles the form submission for updating an existing movie's details.

    Args:
        user_id (int): The ID of the user who owns the movie.
        movie_id (int): The ID of the movie to be updated.
    """
    user = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_by_id(movie_id)

    if not user or not movie or movie.user_id != user_id:
        flash("Movie or user not found, or movie doesn't belong to user.", 'error') # Flash message
        return redirect(url_for('home'))

    new_name = request.form.get('movie_name')
    new_director = request.form.get('director')
    new_year_str = request.form.get('year')

    new_year = int(new_year_str) if new_year_str and new_year_str.isdigit() else None

    if new_name and new_director:
        updated_movie = data_manager.update_movie(movie_id, new_name, new_director, new_year)
        if updated_movie:
            flash(f"Movie '{updated_movie.name}' updated successfully!", 'success') # Flash message
        else:
            flash("Failed to update movie.", 'error') # Flash message
    else:
        flash("Movie name or director cannot be empty for update.", 'error') # Flash message

    return redirect(url_for('list_user_movies', user_id=user.id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id: int, movie_id: int):
    """
    Handles the POST request to delete a specific movie from a user's list.

    Args:
        user_id (int): The ID of the user who owns the movie.
        movie_id (int): The ID of the movie to be deleted.
    """
    user = data_manager.get_user_by_id(user_id)
    movie = data_manager.get_movie_by_id(movie_id)

    if user and movie and movie.user_id == user_id:
        if data_manager.delete_movie(movie_id):
            flash(f"Movie '{movie.name}' deleted successfully!", 'success') # Flash message
        else:
            flash("Failed to delete movie.", 'error') # Flash message
    else:
        print(f"Attempted to delete movie {movie_id} for user {user_id} but conditions not met.")
        flash("Movie or user not found, or movie doesn't belong to user.", 'error') # Flash message

    return redirect(url_for('list_user_movies', user_id=user_id))


# Add this error handler at the end of app.py, before if __name__ == '__main__':
@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 Not Found errors, rendering a custom 404.html template.
    """
    return render_template('404.html'), 404 # Returns the template and the 404 status code


# Main entry point for running the Flask application.
if __name__ == '__main__':
    app.run(debug=True)