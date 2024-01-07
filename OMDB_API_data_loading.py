import requests
import logging
import pymysql.err
from SQL_data_loading import parse_movie_name_and_year

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

class DbInterface():
    def __init__(self,data,session):
        self.session = session
        self.data = data
        self.movie_array = None
        self.join_movie_data()

    def join_movie_data(self):
        my_fixed_data = self.data['movie_name'].apply(lambda x: parse_movie_name_and_year(x))
        my_movie_array = my_fixed_data.apply(lambda x: Movie(x[0], x[1], self.session)).unique()
        self.movie_array = my_movie_array




def load_OMDB_data(db_interface): # connection, session):
    """
    Fetches movies from the database with missing OMDB data, and retrieves the data
    using the OMDB API, and then updates the database with this information.

    :param connection: A pymysql connection object used for database operations.
    :param session: A session object to interact with the OMDB API.
    :return: None. The function updates the database and handles exceptions internally.
    """
    my_interface = DbInterface(db_interface['connection'],db_interface['session'])

    return my_interface