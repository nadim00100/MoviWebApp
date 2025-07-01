from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the MoviWeb App.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        name (str): The user's name, must be unique.
        movies (list): A list of Movie objects associated with this user.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the User object.
        """
        return f'<User {self.name}>'

class Movie(db.Model):
    """
    Represents a movie in a user's favorite list.

    Attributes:
        id (int): Primary key, unique identifier for the movie.
        name (str): The title of the movie.
        director (str): The director of the movie (can be null).
        year (int): The release year of the movie (can be null).
        poster_url (str): URL to the movie's poster image (can be null).
        user_id (int): Foreign key linking the movie to a specific user.
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(120), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    poster_url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the Movie object.
        """
        return f'<Movie {self.name} ({self.year})>'