import json
from multiprocessing import Pool
import logging
import Selenium_functions
import argparse
import Create_SQL_database_structure
import SQL_data_loading
import OMDB_API_data_loading
import pymysql

log_filename = 'Propstore.log'
config_filename = "config.json"

logging.basicConfig(filename=log_filename,
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)


def load_config(config_filename):
    """
    Function to read json configuration file
    :param config_filename: the respective configuration file with key variables
    :return: json_dict that contains key variables
    """
    with open(config_filename, "r") as json_file:
        json_dict = json.load(json_file)
        return json_dict


def parse_argument(config):
    """
    Parse command-line arguments for Propstore scraping.
    :return: argparse.Namespace: An object containing parsed arguments.
    """

    parser = argparse.ArgumentParser(description=config["argparse_help_text"])
    parser.add_argument("--all", action="store_true", help="Scrape everything")
    parser.add_argument("--categories", nargs="+",
                        help="Specify categories to scrape. Note if wrong categories are given, they will be ignored")
    parser.add_argument("--live", action="store_true", help="Only scrape live items")
    parser.add_argument("--sold", action="store_true", help="Only scrape already sold items")
    return parser.parse_args()


def scrape_select_categories(url, categories, full_category_list):
    """
    Select categories from the given list that are present in the full category list and construct corresponding URLs.
    :param url: The base URL to replace for category URLs.
    :param categories: List of categories to filter.
    :param full_category_list: Full list of available categories.
    :return: List of category URLs based on the selected categories.
    """
    select_category_list = [category for category in categories if category in full_category_list]
    category_url_list = [url.replace("products", f"category/{category}") for category in select_category_list]
    return category_url_list


def main():
    """
    main function to open Propstore.com through Selenium, scroll to the bottom of the page, and take relevant movie information
    :return: key movie information (Movie name, item name, price, and category) from Propstore.com in dictionary format
    """
    config = load_config(config_filename)
    url = config["url"]
    username = config["username"]
    password = config["password"]

    args = parse_argument(config)

    if args.all:
        category_url_list = scrape_select_categories(url, config["category_list"], config["category_list"])
        categories = " ".join(config["category_list"])
    elif args.categories:
        category_url_list = scrape_select_categories(url, args.categories, config["category_list"])
        categories = " ".join(args.categories)
    else:
        print("Please provide valid arguments. Use --help for more info.")

    try:
        option = "live_items" if args.live else "sold_items" if args.sold else "all_items"
        logging.info(f"Scraping {option} on Propstore.com for {categories}")
        print(f"Scraping {option} on Propstore.com for {categories}")
        connection_without_database = pymysql.connect(host=config["SQL_host"], user=config["SQL_user"],
                                                      password=config["SQL_password"],
                                                      cursorclass=pymysql.cursors.DictCursor)
        Create_SQL_database_structure.create_database(config,connection_without_database)
        connection = SQL_data_loading.get_connection(config)
        with Pool() as pool:
            items_list = pool.starmap(Selenium_functions.process_category,
                                   [(category_url, username, password, option, config) for category_url in
                                    category_url_list])
            for item in items_list:
                SQL_data_loading.load_data(item, connection)

        omdb_session = OMDB_API_data_loading.create_omdb_session(config["OMDB_api_key"])
        OMDB_API_data_loading.OMDB_data_loading(connection,omdb_session,config["OMDB_api_key"])


    except UnboundLocalError as error:
        logging.error(f"Error: {error}")
        print(f"Please define the scrape method")



if __name__ == "__main__":
    main()
