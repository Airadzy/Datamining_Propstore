import requests

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
    def __init__(self, movie_name, year, session, api_key):
        self.movie_name = movie_name
        self.year = year
        self.session = session
        self.api_key = api_key

    def info(self):
        path = f"http://www.omdbapi.com/?t={self.movie_name}&y={self.year}&apikey={self.api_key}"
        response = self.session.get(path)
        return response.json()


def OMDB_data_loading(connection, session, api_key):
    try:
        with connection.cursor() as cursor:
            cursor.execute("Select * from movies WHERE API_title IS NULL;")
            movies = cursor.fetchall()

            for movie in movies:
                movie_info = Movie(movie["movies_name"], movie["release_year"], session, api_key).info()
                if movie_info['Response'] == "False":
                    print(
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
            print("All OMDB movies inserted into database")
    except Exception as error:
        print(f"An error occurred: {error}")
    finally:
        connection.close()
