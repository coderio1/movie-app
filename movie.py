# Standard library imports
import os
import random
import statistics

# Storage layer
import movie_storage

# Plotting
import matplotlib.pyplot as plt

# Terminal colors
from colorama import Fore, Back, Style, init

# Fuzzy string matching
from thefuzz import process

# Automate color reset after every print
init(autoreset=True)

def list_menu():
    """List the menu options"""
    print(
        "****************************\n"
        "***CINEMA MOVIES DATABASE***\n"
        "++++++++++++++++++++++++++++"
    )
    print(Back.MAGENTA + "Menu:")
    menu = [
        "Exit", "List movies", "Add movie", "Delete movie",
        "Update movie", "Stats", "Random movie", "Search movie",
        "Movie sorted by rating", "Save histogram",
        "Movie sorted by year"
    ]
    numbers = [
        "0.", "1.", "2.", "3.", "4.", "5.", "6.",
        "7.", "8.", "9.", "10."
    ]
    for item, num in zip(menu, numbers):
        print(Back.MAGENTA + num, item)
    print("")


def select_menu_options():
    """User input for menu selection"""

    select_option = int(
        input(Back.GREEN + "enter your choice (number 0-10): "
              + Style.RESET_ALL)
    )
    return select_option


def menu_options_logic(num):
    """Options logic."""

    movies = transform_dict_to_list(movie_storage.get_movies())
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
    else:
        print(Back.RED + "Invalid option. Please enter a number between 0 and 10.")


def transform_dict_to_list(enter_dict):
    """Transform dict to a list of (movie, data) tuples."""

    movie_list = list(enter_dict.items())
    return movie_list


def list_movie(movie_list):
    """List all movies from the dictionary"""

    counter = 0
    for movie, data in movie_list:
        counter += 1
        print(
            f"{counter}. {movie} | "
            f"rating: {data['rate']} | year: {data['year']}"
        )
    print("\n")


def add_movie():
    """Add movie to the list"""

    add_new_movie = input(Fore.BLUE + "Add a new movie on the list: ")
    if add_new_movie not in movie_storage.get_movies():
        try:
            add_rating = float(input("Enter movie rating (0-10): "))
            add_year = int(input("Enter release year: "))
        except ValueError:
            print("Error: Invalid input.\n")
            return
        movie_storage.add_movie(add_new_movie, add_rating, add_year)
        print(
            Back.GREEN +
            f"movie {add_new_movie} successfully added\n" +
            Style.RESET_ALL
        )
    else:
        print(
            Back.RED +
            f"movie {add_new_movie} already exists in the list\n" +
            Style.RESET_ALL
        )


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
            f"{update_movie} rating has been successfully updated\n" +
            Style.RESET_ALL
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


def main():
    """Main program loop"""
    movies = {
        "The Shawshank Redemption": {"rate": 9.5,  "year": 1994},
        "Pulp Fiction":             {"rate": 8.8,  "year": 1994},
        "The Room":                 {"rate": 3.6,  "year": 2003},
        "Matrix":                   {"rate": 8.44, "year": 1999},
        "The Godfather":            {"rate": 9.2,  "year": 1972},
        "The Godfather: Part II":   {"rate": 9.0,  "year": 1974},
        "The Dark Knight":          {"rate": 9.0,  "year": 2008},
        "12 Angry Men":             {"rate": 8.9,  "year": 1957},
        "Everything Everywhere All At Once": {"rate": 8.9, "year": 2022},
        "Forrest Gump":             {"rate": 8.8,  "year": 1994},
        "Star Wars: Episode V":     {"rate": 8.7,  "year": 1980},
    }

    # Check if file already exists, write if not
    if not os.path.isfile("data.json"):
        movie_storage.save_movies(movies)
    else:
        print("File already exists!!!")

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
