# data_manager.py
"""
This module defines the DataManager class for handling database operations
related to users and movies within the MoviWeb application.
"""

from models import db, User, Movie


class DataManager:
    """
    Manages all Create, Read, Update, and Delete (CRUD) operations
    for users and movies in the database using SQLAlchemy ORM.
    """

    def create_user(self, name: str) -> User:
        """
        Adds a new user to the database.

        Args:
            name (str): The name of the user to create.

                                Returns:
            User: The newly created User object.
        """
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_users(self) -> list[User]:
        """
        Retrieves a list of all users from the database.

        Returns:
            list[User]: A list of User objects.
        """
        return User.query.all()

    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieves a user by their ID from the database.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: The User object if found, otherwise None.
        """
        return User.query.get(user_id)

    def get_movies(self, user_id: int) -> list[Movie]:
        """
        Retrieves a list of all movies for a specific user from the database.

        Args:
            user_id (int): The ID of the user whose movies to retrieve.

        Returns:
            list[Movie]: A list of Movie objects belonging to the specified user.
        """
        user = self.get_user_by_id(user_id)
        if user:
            # 'movies' is the relationship defined in the User model
            return user.movies
        return []

    def add_movie(self, movie: Movie) -> Movie:
        """
        Adds a new movie to a user's favorite list in the database.

        Args:
            movie (Movie): The Movie object to add. This object should
                           already have its user_id set.

        Returns:
            Movie: The newly added Movie object.
        """
        db.session.add(movie)
        db.session.commit()
        return movie

    def update_movie(self, movie_id: int, new_name: str = None,
                     new_director: str = None, new_year: int = None,
                     new_poster_url: str = None) -> Movie | None:
        """
        Updates the details of a specific movie in the database.

        Args:
            movie_id (int): The ID of the movie to update.
            new_name (str, optional): The new title of the movie.
            new_director (str, optional): The new director of the movie.
            new_year (int, optional): The new release year of the movie.
            new_poster_url (str, optional): The new poster URL of the movie.

        Returns:
            Movie | None: The updated Movie object if found, otherwise None.
        """
        movie = Movie.query.get(movie_id)
        if movie:
            if new_name is not None:
                movie.name = new_name
            if new_director is not None:
                movie.director = new_director
            if new_year is not None:
                movie.year = new_year
            if new_poster_url is not None:
                movie.poster_url = new_poster_url
            db.session.commit()
            return movie
        return None

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