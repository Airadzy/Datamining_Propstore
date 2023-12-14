from bs4 import BeautifulSoup
import csv
from pathlib import Path
import logging


def extract_to_csv(items_list, category, config):
    """
    Write data from the items_list into a CSV file.
    :param items_list: List containing category items and details.
    :param category: Category for which data is being written to the CSV file.
    :return: None
    """
    path = Path(config["csv_file_path"])
    try:
        if not items_list:
            logging.warning(config["empty_item_list_warning"])
            print(config["empty_item_list_warning"])
        field_names = config["field_names"]
        mode = "w" if not path.exists() else "a"
        with open(path, mode, newline="") as file:
            writer = csv.writer(file)
            if mode == "w":
                writer.writerow(field_names)
            writer.writerows(items_list)
        logging.info(f"Successfully inserted into csv file data from {category}")
        print(f"Successfully inserted into csv file data from {category}")
    except Exception as error:
        logging.error(config["csv_error_message"])
        print(config["csv_error_message"])
    finally:
        pass


def extract_data(html_content, category_url, option, config):
    """
    Extract movie name, sale date and price (either sold or offer if live) from website
    :param html_content: The HTML content of the webpage.
    :param category_url: The URL of the category.
    :param option: The scraping option (live_items, sold_items, all_items).
    :param config (dict): Configuration dictionary containing messages and settings.
    :return: n/a
    """
    try:
        button_dict = config["button_dict"]

        soup = BeautifulSoup(html_content, "html.parser")
        cards = soup.find_all("div", class_="card__info")
        items_set = set()
        category = category_url.split("/")[4]
        for number, card in enumerate(cards):
            try:
                button = card.find("button").text.strip()
                movie_name = card.find("div", class_="card__movie").text.strip()
                card_title = " ".join(card.find("div", class_="card__title").text.strip().split())
                price_element = card.find("span", class_="card__price-title")
                price = price_element.text.strip() if price_element else None
                sold_date_element = card.find("span", class_="card__price-soldon")
                sold_date = sold_date_element.text.strip() if sold_date_element else None

                item_tuple = (button, category, movie_name, card_title, price, sold_date)
                if item_tuple not in items_set and button in button_dict[option]:
                    items_set.add(item_tuple)
            except Exception as error:
                logging.error(f"Error in extracting data: {error} in {card.text}")
                print(f"Error in extracting data: {error} in {card.text}")
                continue

        items_list = list(items_set)
        print(f"FINISHED EXTRACTING {category}. Number of items fetched: {len(items_list)}")
        logging.info(f"FINISHED EXTRACTING {category}. Number of items fetched: {len(items_list)}")
        extract_to_csv(items_list, category, config)

    except Exception as error:
        logging.error(f"Error in extract_data: {error}")
        print(f"Error in extract_data: {error}")
