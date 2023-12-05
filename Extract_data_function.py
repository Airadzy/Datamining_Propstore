from bs4 import BeautifulSoup
import logging
import csv

def extract_to_csv(items_list):
    header_names = ["id","category","movie_name","card_title","price"]
    with open("Propstore_data.csv","w") as propstore_csv_file:
        writer = csv.DictWriter(propstore_csv_file,fieldnames=header_names)
        writer.writeheader()
        for row in reader

def extract_data(html_content, category_url):
    """
    Extract movie name, sale date and price (either sold or offer if live) from website
    :param html_content:
    :param category_url:
    :return:
    """
    soup = BeautifulSoup(html_content, "html.parser")
    cards = soup.find_all("div", class_="card__info")
    items_list = []
    for number, card in enumerate(cards):
        try:
            category = category_url.split("/")[4]
            movie_name = card.find("div", class_="card__movie").text.strip()
            card_title = card.find("div", class_="card__title").text.strip()
            card_title = " ".join(card_title.split())
            price = card.find("span", class_="card__price-title").text.strip()
            item_dict = {"category": {category},"movie_name":{movie_name},"card_title":{card_title},"price": {price}}
            items_list.append(item_dict)
        except Exception as error:
            print(f"error {error}")
            continue
    logging.info(f"\nCreated dict from {category} with: {len(card_dict)} items\n")
    print(items_list)


def main():
    print("No relevance to this function standalone")


if __name__ == "__main__":
    main()
