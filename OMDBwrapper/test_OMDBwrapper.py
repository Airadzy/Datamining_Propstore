from OMDBwrapper import movie
import vcr

@vcr.use_cassette("vcr_cassettes/movie_info.yml")
def test_movie_info():
    """Tests an API call to get a TV show's info"""

    movie_instance = movie("Star Wars",2015)
    response = movie_instance.info()
    print(response)

    assert isinstance(response, dict)
    assert movie_instance.movie_name == "Star Wars"
    assert movie_instance.year == 2015