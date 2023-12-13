import json
from multiprocessing import Pool
import logging
import Selenium_functions
import argparse

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


def scrape_all_categories(url):
    """
    function to create  urls for each category on Propstore page
    :param url: main url from Propstore website
    :return: list of urls for each prop category
    """
    category_list = ["props", "costumes", "artwork", "posters", "toys", "production", "autographs",
                     "promotional-items"]  # "props","costumes","artwork","posters","toys","production","autographs","promotional-items"
    category_url_list = [url.replace("products", f"category/{category}") for category in category_list]
    return category_url_list

def scrape_select_categories(url,categories):
    full_category_list = ["props", "costumes", "artwork", "posters", "toys", "production", "autographs",
                     "promotional-items"]
    select_category_list = []
    for category in categories:
        if category not in full_category_list:
            print(f"Warning: The category '{category}' doesn't exist or has not been included. Skipping...")
        else:
            select_category_list.append(category)

    category_url_list = [url.replace("products", f"category/{category}") for category in select_category_list]
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

    parser = argparse.ArgumentParser(
        description="Welcome to the Propstore mining tool. Please enter your desired items to be scraped in this format: function item_#1_to_be scraped item_#2_to_be_scraped ...")

    parser.add_argument("--all", action="store_true", help="Scrape everything")
    parser.add_argument("--categories", nargs="+",
                        help="Specify categories to scrape (can choose multiple): props, costumes, artwork, posters, toys, production, autographs, promotional-items")
    # parser.add_argument("-__previous",action="store_true",help="Only scrape items that have already been sold (not currently live ones)")
    # parser.add_argument("-__live", action="store_true", help="Only scrape items that are  currently live on website")
    args = parser.parse_args()

    if args.all:
        category_url_list = scrape_all_categories(url)
    elif args.categories:
        category_url_list = scrape_select_categories(url,args.categories)
    else:
        print("Please provide valid arguments. Use --help for more info.")


    with Pool() as pool:
        pool.starmap(Selenium_functions.process_category,
                     [(category_url, username, password) for category_url in category_url_list])


if __name__ == "__main__":
    main()
