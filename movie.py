# Standard library imports
import random
import statistics
import os

# HTTP requests
import requests

# Storage layer DB
import movie_storage

OMDB_API_KEY = "34ee7f0f"
OMDB_URL = "http://www.omdbapi.com/"

# Plotting
import matplotlib.pyplot as plt

# Terminal colors
from colorama import Fore, Back, Style, init

# Fuzzy string matching
from thefuzz import process

# Automate color reset after every print
init(autoreset=True)

def fetch_movie_from_omdb(title):
    """Fetch movie rating and year from OMDb API by title."""
    response = requests.get(OMDB_URL, params={"t": title, "apikey": OMDB_API_KEY})
    data = response.json()

    if data.get("Response") == "False":
        print(Back.RED + f"OMDb: movie '{title}' not found.")
        return None

    try:
        omdb_title = data["Title"]
        rating = float(data["imdbRating"])
        year = int(data["Year"][:4])
        poster = data["Poster"]
    except (KeyError, ValueError):
        print(Back.RED + "OMDb: could not parse movie data.")
        return None

    return omdb_title, rating, year, poster


def list_menu():
    """List the menu options"""
    print(
        "****************************\n"
        "***CINEMA MOVIES DATABASE***\n"
        "++++++++++++++++++++++++++++"
    )
    print(Back.MAGENTA + "Menu:")

    # menu dynamic enumerating
    menu = [
        "Exit", "List movies", "Add movie", "Delete movie",
        "Update movie", "Stats", "Random movie", "Search movie",
        "Movie sorted by rating", "Save histogram",
        "Movie sorted by year", "Generate website"
    ]
    for num, item in enumerate(menu):
        print(Back.MAGENTA + f"{num}. {item}")
    print("")


def select_menu_options():
    """User input for menu selection"""

    select_option = int(
        input(Back.GREEN + "enter your choice (number 0-11): "
              + Style.RESET_ALL)
    )
    return select_option


def menu_options_logic(num):
    """Options logic."""

    movies = list(movie_storage.get_movies().items())
    if num == 1:
        list_movie(movies)
    elif num == 2:
        add_movie()
    elif num == 3:
        delete_movie()
    elif num == 4:
        update_movie_rating()
    elif num == 5:
        (best_rating, best_movie,
         mean_rating, avg_rating,
         worst_rating, worst_movie) = statistics_movie(
            sorted_by_rating_movie(movies)
        )
        print(
            Back.BLUE +
            f"The best rating: {best_movie} {best_rating:.1f}\n"
            f"Mean rating: {mean_rating:.1f}\n"
            f"Median rating: {avg_rating:.1f}\n"
            f"The worst rating: {worst_movie} {worst_rating:.1f}"
        )
    elif num == 6:
        recommendation_movie(movies)
    elif num == 7:
        search_movie(movies)
    elif num == 8:
        list_movie(sorted_by_rating_movie(movies))
    elif num == 9:
        create_rating_histogram(movies)
    elif num == 10:
        list_movie(sorted_by_year_movie(movies))
    elif num == 11:
        generate_website(movies)
    else:
        print(Back.RED + "Invalid option. Please enter a number between 0 and 11.")


def list_movie(movie_list):
    """List all movies from DB"""

    counter = 0
    for movie, data in movie_list:
        counter += 1
        print(
            f"{counter}. {movie} | "
            f"rating: {data['rate']} | year: {data['year']} | poster: {data['poster']} "
        )
    print("\n")


def add_movie():
    """Fetch movie, rating, year from OMDb API and adds movie to the list"""
    query = input(Fore.BLUE + "Add a new movie on the list: ").strip()

    if not query:
        print(Back.RED + "Error: Movie title cannot be empty.\n")
        return

    if query in movie_storage.get_movies():
        print(Back.RED + f"movie '{query}' already exists in the list\n")
        return

    try:
        result = fetch_movie_from_omdb(query)
    except requests.exceptions.ConnectionError:
        print(Back.RED + "Error: No internet connection. Could not reach OMDb.\n")
        return
    except requests.exceptions.Timeout:
        print(Back.RED + "Error: Request timed out. Try again later.\n")
        return
    except requests.exceptions.RequestException as e:
        print(Back.RED + f"Error: API request failed: {e}\n")
        return

    if result is None:
        return

    title, rating, year, poster = result
    try:
        movie_storage.add_movie(title, rating, year, poster)
    except Exception as e:
        print(Back.RED + f"Error: Could not save movie to database: {e}\n")
        return

    print(Back.GREEN + f"'{title}' ({year}) rated {rating} successfully added\n")


def delete_movie():
    """Delete movie from the list"""

    movie_to_delete = input("Delete a movie from the list: ")
    if movie_to_delete in movie_storage.get_movies():
        movie_storage.delete_movie(movie_to_delete)
        print(f"movie, {movie_to_delete} successfully deleted!\n")
    else:
        print(
            Back.RED +
            f"Error: {movie_to_delete} is not existing in the list"
        )


def update_movie_rating():
    """Update movie rating in the list"""

    update_movie = input("Enter movie name: ")
    if update_movie in movie_storage.get_movies():
        try:
            new_rating = float(input("Enter new rating (0-10): "))
        except ValueError:
            print("Error: Rating must be a decimal number.\n")
            return
        movie_storage.update_movie(update_movie, new_rating)
        print(
            Back.GREEN +
            f"{update_movie} rating has been successfully updated\n"
        )
    else:
        print(Back.RED + f"Error: {update_movie} is not existing in the list")


def recommendation_movie(movie_list):
    """Pick and display a random movie recommendation"""

    recommendation = random.randint(0, len(movie_list) - 1)
    movie, data = movie_list[recommendation]
    print(
        Fore.BLUE +
        f"Recommended movie for tonight is >>{movie}<< "
        f"with rating >>{data['rate']}<< ({data['year']})\n" +
        Style.RESET_ALL
    )


def search_movie(movie_list):
    """Fuzzy search engine using thefuzz"""

    query = input("Search movie: ")
    movie_names = [movie for movie, data in movie_list]
    matches = process.extract(query, movie_names, limit=3)

    best_match, best_score = matches[0]

    if best_score >= 90:
        # Exact match
        data = [data for movie, data in movie_list if movie == best_match][0]
        print(f"\n Found: {best_match} ({data['rate']} <>, {data['year']})")
    elif best_score >= 60:
        # Similar movies
        print(f"\n '{query}' not found. Did you mean:")
        for movie, score in matches:
            if score >= 60:
                data = [d for m, d in movie_list if m == movie][0]
                print(
                    f"{movie} ({data['rate']} <>, {data['year']}) "
                    f"- {score}% match"
                )
    else:
        # No match
        print(f"\n '{query}' not found. No similar movies.")


def sorted_by_rating_movie(movie_list):
    """Sort movies by rating in descending order"""

    sorted_list_desc = sorted(
        movie_list, key=lambda x: x[1]["rate"], reverse=True
    )
    return sorted_list_desc


def sorted_by_year_movie(movie_list):
    """Sort movies by release year in ascending order"""

    sorted_list_asc = sorted(movie_list, key=lambda x: x[1]["year"])
    return sorted_list_asc


def statistics_movie(movie_list):
    """Return statistics for the movie list"""

    ratings = [data["rate"] for movie, data in movie_list]
    best_rating = max(ratings)
    worst_rating = min(ratings)
    mean_rating = statistics.mean(ratings)
    avg_rating = statistics.median(ratings)

    best_movie = [
        movie for movie, data in movie_list if data["rate"] == best_rating
    ][0]
    worst_movie = [
        movie for movie, data in movie_list if data["rate"] == worst_rating
    ][0]

    return (
        best_rating, best_movie,
        mean_rating, avg_rating,
        worst_rating, worst_movie
    )


def create_rating_histogram(movie_list):
    """Create and save a histogram of movie ratings"""

    ratings = [data["rate"] for movie, data in movie_list]

    # Ask user for filename
    filename = input(
        "\nEnter filename to save histogram (e.g., 'histogram.png'): "
    ).strip()

    # Add .png extension if not provided
    if not filename.endswith(('.png', '.jpg', '.pdf', '.svg')):
        filename += '.png'

    # Save in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, filename)

    # Create histogram
    plt.figure(figsize=(12, 7))
    plt.hist(ratings, bins=10, edgecolor='black', color='skyblue', alpha=0.7)
    plt.xlabel('Rating', fontsize=12)
    plt.ylabel('Number of Movies', fontsize=12)
    plt.title('Movie Ratings Distribution', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.xticks(range(0, 11))
    plt.tight_layout()

    # Save to file
    try:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n✓ Histogram saved successfully to:\n  {filename}")
        plt.close()
    except Exception as e:
        print(Back.RED + f"\n✗ Error saving histogram: {e}")
        plt.close()


def generate_website(movie_list):
    """Generate an HTML web by means of movies_template.html.
    Lists movies with posters and ratings"""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "movies_template.html")
    output_path = os.path.join(script_dir, "movies.html")

    try:
        with open(template_path, "r") as f:
            template = f.read()
    except FileNotFoundError:
        print(Back.RED + "Error: movies_template.html not found.\n")
        return

    cards_html = ""
    for title, data in movie_list:
        if data.get("poster") and data["poster"] != "N/A":
            image_tag = f'<img class="card__poster" src="{data["poster"]}" alt="{title} poster">'
        else:
            image_tag = '<div class="card__poster--placeholder">🎬</div>'

        cards_html += (
            f'<li class="card">\n'
            f'    {image_tag}\n'
            f'    <div class="card__body">\n'
            f'        <p class="card__title">{title}</p>\n'
            f'        <p class="card__year">{data["year"]}</p>\n'
            f'        <p class="card__rating">{data["rate"]}</p>\n'
            f'    </div>\n'
            f'</li>\n'
        )

    html = template.replace("__REPLACE_MOVIE_CARDS__", cards_html)

    try:
        with open(output_path, "w") as f:
            f.write(html)
        print(Back.GREEN + f"Website generated: {output_path}\n")
    except Exception as e:
        print(Back.RED + f"Error: Could not write website: {e}\n")


def main():
    """Main program loop"""
    # Display menu
    list_menu()

    while True:
        try:
            user_select = select_menu_options()
            if user_select == 0:
                print("\n.....closing the program....\nBye Bye!")
                break
            else:
                menu_options_logic(user_select)
        except ValueError:
            print("\nOnly numbers are accepted\n")
        except IndexError:
            print("\nError: Try again!")

        input(Back.YELLOW + "Press >>Enter<< to continue")
        list_menu()


if __name__ == "__main__":
    main()
