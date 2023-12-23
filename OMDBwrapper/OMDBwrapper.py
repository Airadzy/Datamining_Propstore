import requests
import pymysql

OMDB_API_KEY = "b98bb901"

session = requests.Session()
session.params = {}
session.params["api_key"] = OMDB_API_KEY

class movie:
    def __init__(self,movie_name,year):
        self.movie_name = movie_name
        self.year = year

    def info(self):
        path = f"http://www.omdbapi.com/?t={self.movie_name}&y={self.year}&apikey={OMDB_API_KEY}"
        response = session.get(path)
        return response.json()
