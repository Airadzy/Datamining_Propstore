from bs4 import BeautifulSoup
import logging
import csv
from pathlib import Path


def extract_to_csv(items_list,category):
    """
    function to take data created in extract_data function and write into a csv file
    :param items_list: list with category items and details
    :return:
    """

    try:
        path = Path("./Propstore_data.csv")

        if not items_list:
            logging.warning("items_list is empty. NO CSV file created.")
            return

        field_names = ["category", "movie_name", "card_title", "price"]
        if path.exists() is not True:
            with open("Propstore_data.csv", "w",newline="") as file:
                writer = csv.writer(file)
                writer.writerow(field_names)
                writer.writerows(items_list)
        else:
            with open("Propstore_data.csv", "a",newline="") as file:
                writer = csv.writer(file)
                writer.writerows(items_list)
        logging.info(f"\nSuccessfully created csv file from {category}\n")
        return f"\nSuccessfully created csv file from {category}\n"
    except Exception as error:
        print(f"ERROR IN WRITE CSV FILE: {error}")


def extract_data(html_content, category_url):
    """
    Extract movie name, sale date and price (either sold or offer if live) from website
    :param html_content:
    :param category_url:
    :return: n/a
    """
    soup = BeautifulSoup(html_content, "html.parser")
    cards = soup.find_all("div", class_="card__info")
    items_set = set()
    category = category_url.split("/")[4]
    for number, card in enumerate(cards):
        try:
            movie_name = card.find("div", class_="card__movie").text.strip()
            card_title = card.find("div", class_="card__title").text.strip()
            card_title = " ".join(card_title.split())
            price_element = card.find("span", class_="card__price-title")
            price = price_element.text.strip() if price_element else None
            item_tuple = (category, movie_name, card_title, price)
            if item_tuple not in items_set:
                items_set.add(item_tuple)
        except Exception as error:
            print(f"ERROR in EXTRACT DATA {error} in {card.text}")
            continue
    items_list = list(items_set)
    logging.info(f"\nSuccessfully created dict from {category} with: {len(items_list)} items\n")
    extract_to_csv(items_list,category)
    return f"\nSuccessfully created dict from {category} with: {len(items_list)} items\n"


def main():
    print("No relevance to this function standalone")


if __name__ == "__main__":
    main()
