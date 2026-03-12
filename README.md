# Movie Database and Recommendation Program

---

## General

This is a Python project that works with an SQL database, HTML, and API calls to store information about movies, make movie recommendations, and generate statistics. Users can expand its functionality by adding new movies or correcting existing rating statistics.

---

## Features

- Store and retrieve movie information using an SQL database
- Add new movies to the database
- Delete movies from the database
- Update movie information
- Generate statistics about the movie collection
- Get a random movie recommendation
- Search for movies based on title or other criteria
- Sort movies by their rating
- Generate an HTML website to showcase the movie database

---

## Prerequisits to install

In order to be able to run the python program properly, ensure that `thefuzz`,`colorama`,`sqlalchemy` packages are installed.<br>
If the packages are missing, simply run the commands in your terminal:

```bash
pip install thefuzz
pip install colorama
pip install sqlalchemy
```

---

## Setup

To set up the project, follow these steps:
1. Open your terminal
2. Clone the project repository to your working directory using `git clone`
```bash
git clone https://github.com/coderio1/movie-app.git
```
3. Navigate to the project directory and start the program by running the `./movies.py` script
```bash
python3 movie.py
```
---

## Usage

To use the program, run the `./movies.py` script and select the desired option from the menu by entering the corresponding number and pressing Enter on your keyboard. The available options are:

&nbsp; &nbsp; 0 - Exit </br>
&nbsp; &nbsp; 1 - List movies </br>
&nbsp; &nbsp; 2 - Add movie </br>
&nbsp; &nbsp; 3 - Delete movie </br>
&nbsp; &nbsp; 4 - Update movie </br>
&nbsp; &nbsp; 5 - Stats </br>
&nbsp; &nbsp; 6 - Random movie </br>
&nbsp; &nbsp; 7 - Search movie </br>
&nbsp; &nbsp; 8 - Movies sorted by rating </br>
&nbsp; &nbsp; 9 - Save histogram </br>
&nbsp; &nbsp; 10 - Movies sorted by year </br>
&nbsp; &nbsp; 11 - Generate website </br>

---
 
## Project Structure
 
```
movie-app/
├── data/moviedb.sqlite3      # SQLite database
├── movie.py                  # Main Python script
├── movie_storage.py          # Script for DB manipulation
└── movies_template.html      # Template to generate website
```

---

## Technologies Used

- Python
- SQL (SQLite)
- HTML
- API calls (OMDb)

---

## Contributing

If you would like to contribute to this project, please follow these steps:
1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with descriptive messages
4. Push your changes to your forked repository
5. Submit a pull request detailing your changes

---
