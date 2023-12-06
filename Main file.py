import json
from multiprocessing import Pool
import logging
import Selenium_functions

logging.basicConfig(filename='Propstore.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def read_config():
    """
    function to read json configuration file
    :return: json_dict that contains key variables
    """
    with open("config.json", "r") as json_file:
        json_dict = json.load(json_file)
        return json_dict


def go_through_categories(url):
    """
    function to create  urls for each category on Propstore page
    :param url: main url from Propstore website
    :return: list of urls for each prop category
    """
    category_list = ["promotional-items"] #"props", "costumes", "artwork", "posters", "toys", "production", "autographs",
    category_url_list = [url.replace("products", f"category/{category}") for category in category_list]
    return category_url_list


def main():
    """
    main function to open Propstore.com through Selenium, scroll to the bottom of the page, and take relevant movie information
    :return: key movie information (Movie name, item name, price, and category) from Propstore.com in dictionary format
    """

    config = read_config()
    url = config["url"]
    username = config["username"]
    password = config["password"]

    category_url_list = go_through_categories(url)
    with Pool() as pool:
        pool.starmap(Selenium_functions.process_category,
                     [(category_url, username, password) for category_url in category_url_list])


if __name__ == "__main__":
    main()
