# data_manager.py
"""
Manages database operations for the MoviWeb App using SQLAlchemy.
Provides methods for CRUD operations on User and Movie objects.
"""

from models import db, User, Movie
from typing import List, Optional

class DataManager:
    """
    Handles basic CRUD operations for the User and Movie models.
    """

    def create_user(self, name: str) -> User:
        """
        Adds a new user to the database.

        Args:
            name (str): The name of the user.

        Returns:
            User: The newly created User object.
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self) -> List[User]:
        """
        Returns a list of all users in the database.

        Returns:
            List[User]: A list of User objects.
        """
        return User.query.all()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[User]: The User object if found, otherwise None.
        """
        return User.query.get(user_id)

    def get_movies(self, user_id: int) -> List[Movie]:
        """
        Returns a list of all movies for a specific user.

        Args:
            user_id (int): The ID of the user whose movies to retrieve.

        Returns:
            List[Movie]: A list of Movie objects belonging to the user.
        """
        # Ensure the user exists before querying for movies
        user = User.query.get(user_id)
        if user:
            return user.movies # Access the relationship
        return []

    def add_movie(self, movie: Movie) -> None:
        """
        Adds a new movie to a user's favorites in the database.

        Args:
            movie (Movie): The Movie object to add. It should already have a user_id.
        """
        db.session.add(movie)
        db.session.commit()

    def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        """
        Retrieves a movie by its ID from the database.

        Args:
            movie_id (int): The ID of the movie to retrieve.

        Returns:
            Movie | None: The Movie object if found, otherwise None.
        """
        return Movie.query.get(movie_id)

    def update_movie(self, movie_id: int, new_name: str, new_director: str, new_year: Optional[int]) -> Optional[Movie]:
        """
        Updates the details of a specific movie in the database.

        Args:
            movie_id (int): The ID of the movie to update.
            new_name (str): The new title for the movie.
            new_director (str): The new director for the movie.
            new_year (Optional[int]): The new release year for the movie (can be None).

        Returns:
            Optional[Movie]: The updated Movie object if found, otherwise None.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_name
            movie.director = new_director
            movie.year = new_year
            db.session.commit()
        return movie

    def delete_movie(self, movie_id: int) -> bool:
        """
        Deletes a movie from the database.

        Args:
            movie_id (int): The ID of the movie to delete.

        Returns:
            bool: True if the movie was deleted, False otherwise.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False