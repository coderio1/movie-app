import json

DATA_FILE = "data.json"


def get_movies():
    """Load and return movies dict from JSON file"""

    try:
        with open(DATA_FILE, "r") as fileobj:
            return json.load(fileobj)
    except OSError:
        print("File not found or not accessible!")
        return {}
    except json.JSONDecodeError:
        print("Corrupted file!")
        return {}


def save_movies(movies):
    """Write movies dict to JSON file"""

    try:
        with open(DATA_FILE, "w") as fileobj:
            json.dump(movies, fileobj, indent=4)
        # print("...movies successfully saved!")
    except OSError as e:
        print("...save function cannot make change on the disk!",e)


def add_movie(title, rating, year):
    """Add a new movie entry and persist to storage"""

    movies = get_movies()
    movies[title] = {"rate": rating, "year": year}
    save_movies(movies)


def delete_movie(title):
    """Remove a movie by title and persist to storage"""
    movies = get_movies()
    movies.pop(title)
    save_movies(movies)


def update_movie(title, rating):
    """Update a movie's rating and persist to storage"""

    movies = get_movies()
    movies[title]["rate"] = rating
    save_movies(movies)