from bs4 import BeautifulSoup
import logging

def extract_data(html_content, category_url):
    """
    extract movie name, sale date and price (either sold or offer if live) from website
    :param html_content:
    :param category_url:
    :return:
    """
    soup = BeautifulSoup(html_content, "html.parser")
    cards = soup.find_all("div", class_="card__info")
    card_dict = {}
    for number, card in enumerate(cards):
        try:
            category = category_url.split("/")[4]
            movie_name = card.find("div", class_="card__movie").text.strip()
            card_title = card.find("div", class_="card__title").text.strip()
            card_title = " ".join(card_title.split())
            price = card.find("span", class_="card__price-title").text.strip()
            card_dict[number] = [category, movie_name, card_title, price]
        except Exception as error:
            print(f"error {error}")
            continue
    logging.info(f"\nCreated dict from {category} with: {len(card_dict)} items\n")
    print(card_dict)

def main():
    extract_data(input1,input2)

if __name__ =="__main__":
    main()