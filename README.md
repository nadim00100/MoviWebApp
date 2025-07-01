# MoviWeb App

## Project Description
MoviWeb App is a simple Flask-based web application that allows users to manage their favorite movie lists. Users can create accounts, add movies to their personal lists (with details like director, year, and poster fetched from the OMDb API), update movie details, delete movies, and search through their added movies.

## Features
* User Management: Create, view, and list users.
* Movie Management: Add, view, update, and delete movies for each user.
* OMDb API Integration: Automatically fetches movie details (director, year, poster) when a movie is added.
* Search Functionality: Search for movies by title within a user's list.
* Responsive Design: Basic CSS styling for a clean and user-friendly interface.
* Custom 404 Error Page.
* Flash Messaging for user feedback.

## Technologies Used
* **Backend:** Flask (Python Web Framework)
* **Database:** SQLite (managed with Flask-SQLAlchemy)
* **API Integration:** OMDb API (for movie data)
* **Frontend:** HTML, CSS
* **Dependency Management:** `pip` and `requirements.txt`
* **Environment Variables:** `python-dotenv`

## Setup and Installation (Local)

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_GITHUB_USERNAME/MoviWebApp.git](https://github.com/YOUR_GITHUB_USERNAME/MoviWebApp.git)
    # Replace YOUR_GITHUB_USERNAME with your actual GitHub username
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd MoviWebApp
    ```
3.  **Create a Python Virtual Environment:**
    ```bash
    python -m venv venv
    ```
4.  **Activate the virtual environment:**
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    * **Windows (Command Prompt):**
        ```bash
        .\venv\Scripts\activate.bat
        ```
    * **Windows (PowerShell):**
        ```bash
        .\venv\Scripts\Activate.ps1
        ```
5.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Set up your OMDb API Key:**
    * Obtain a free API key from [OMDb API](http://www.omdbapi.com/).
    * Create a file named `.env` in the root of your project directory (if it doesn't exist already).
    * Add your API key to the `.env` file in the following format:
        ```
        OMDB_API_KEY=your_omdb_api_key_here
        SECRET_KEY=a_super_secret_key_for_flask_sessions
        ```
        *(Replace `your_omdb_api_key_here` with your actual key and `a_super_secret_key_for_flask_sessions` with a strong, random string).*
7.  **Run the Flask application:**
    ```bash
    python app.py
    ```
8.  **Access the application:**
    * Open your web browser and go to `http://127.0.0.1:5000/`.

## Deployment
This application can be deployed on platforms like PythonAnywhere. Refer to the deployment instructions for specific steps.

## License
[Optional: Add a license, e.g., MIT License. If you don't add one, it defaults to standard copyright.]

## Author
[Your Name/GitHub Username]
[Optional: Link to your LinkedIn, personal website, etc.]