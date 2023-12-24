import requests
import logging
import pymysql.err

logging.basicConfig(filename="Propstore.log",
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def create_omdb_session(api_key):
    """
    Create and configure a session for OMDB API requests.
    :param api_key: OMDB API key
    :return: Configured session object
    """
    session = requests.Session()
    session.params = {"apikey": api_key}
    return session


class Movie:
    def __init__(self, movie_name, year, session):
        self.movie_name = movie_name
        self.year = year
        self.session = session

    def info(self):
        response = self.session.get("http://www.omdbapi.com/", params={"t": self.movie_name, "y": self.year})
        return response.json()


def load_OMDB_data(connection, session):
    """
    Fetches movies from the database with missing OMDB data, and retrieves the data
    using the OMDB API, and then updates the database with this information.

    :param connection: A pymysql connection object used for database operations.
    :param session: A session object to interact with the OMDB API.
    :return: None. The function updates the database and handles exceptions internally.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("Select * from movies WHERE API_title IS NULL;")
            movies = cursor.fetchmany(10)

            for movie in movies:
                movie_info = Movie(movie["movies_name"], movie["release_year"], session).info()
                if movie_info['Response'] == "False":
                    logging.error(
                        f"Error fetching data for {movie['movies_name']} {movie['release_year']}: {movie_info.get('Error', 'Unknown Error')}")
                    continue
                cursor.execute(
                    "UPDATE movies SET API_title = %s, "
                    "API_year = %s, API_rated = %s,API_runtime = %s,API_genre = %s,"
                    "API_directors = %s,API_country = %s, API_awards = %s,API_rating_imdb = %s,"
                    "API_rating_metascore = %s,API_boxoffice = %s WHERE movies_id = %s",
                    (movie_info.get("Title", None), movie_info.get("Year", None), movie_info.get("Rated", None),
                     movie_info.get("Runtime", None),
                     movie_info.get("Genre", None), movie_info.get("Director", None), movie_info.get("Country", None),
                     movie_info.get("Awards", None),
                     movie_info.get("imdbRating", None), movie_info.get("Metascore", None),
                     movie_info.get("BoxOffice", None), movie["movies_id"]))
        connection.commit()
        logging.info("All OMDB movies inserted into database")
        print("All OMDB movies inserted into database")
    except pymysql.err.OperationalError as error:
        logging.error(f"Operational error in database connection: {error}")
        print(f"Operational error in database connection: {error}")
    except pymysql.err.DatabaseError as error:
        logging.error(f"Database error occurred: {error}")
        print(f"Database error occurred: {error}")
    finally:
        connection.close()
        logging.info("Database connection closed")
