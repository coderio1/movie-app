# import necesarry libraries
import os
from sqlalchemy import create_engine, text

# Build absolute path to the SQLite file
_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "moviedb.sqlite3")
_engine = create_engine(f"sqlite:///{_DB_PATH}")


# Create the table if it doesn't exist
with _engine.connect() as _conn:
    _conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            rate REAL NOT NULL,
            year INTEGER NOT NULL,
            poster TEXT
        )
    """))

def get_movies():
    """Load and return movies from DB"""
    with _engine.connect() as conn:
        rows = conn.execute(text("SELECT title, rate, year, poster FROM movies")).fetchall()
    return {row.title: {"rate": row.rate, "year": row.year, "poster": row.poster} for row in rows}


def add_movie(title, rating, year, poster=None):
    """Add a new movie entry into DB. Create a new table row"""
    with _engine.connect() as conn:
        conn.execute(
            text("INSERT INTO movies (title, rate, year, poster) VALUES (:t, :r, :y, :p)"),
            {"t": title, "r": rating, "y": year, "p": poster}
        )
        conn.commit()



def delete_movie(title):
    """Remove a movie by title from DB. Delete table row"""
    with _engine.connect() as conn:
        conn.execute(text("DELETE FROM movies WHERE title = :t"), {"t": title})
        conn.commit()


def update_movie(title, rating):
    """Update a movie's rating. Update table row"""
    with _engine.connect() as conn:
        conn.execute(
            text("UPDATE movies SET rate = :r WHERE title = :t"),
            {"r": rating, "t": title}
        )
        conn.commit()