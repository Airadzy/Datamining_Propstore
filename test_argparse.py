import argparse

def scrape_all_categories(url):
    """
    function to create  urls for each category on Propstore page
    :param url: main url from Propstore website
    :return: list of urls for each prop category
    """
    category_list = ["props", "costumes", "artwork", "posters", "toys", "production", "autographs",
                     "promotional-items"]  # "props","costumes","artwork","posters","toys","production","autographs","promotional-items"
    category_url_list = ["props", "costumes", "artwork", "posters", "toys", "production", "autographs",
                     "promotional-items"]
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

    category_url_list = select_category_list
    return category_url_list

def main():
    """
    main function to open Propstore.com through Selenium, scroll to the bottom of the page, and take relevant movie information
    :return: key movie information (Movie name, item name, price, and category) from Propstore.com in dictionary format
    """
    url = "https://propstore.com/products/?sortType=5&buyNow=1&archive=1&scroll=220"

    parser = argparse.ArgumentParser(
        description="Welcome to the Propstore mining tool. Please enter your desired items to be scraped in this format: function item_#1_to_be scraped item_#2_to_be_scraped ...")

    parser.add_argument("--all", action="store_true", help="Scrape everything")
    parser.add_argument("--categories", nargs="+",
                        help="Specify categories to scrape (can choose multiple): props, costumes, artwork, posters, toys, production, autographs, promotional-items")
    args = parser.parse_args()

    if args.all:
        category_url_list = scrape_all_categories(url)
        print(category_url_list)
    elif args.categories:
        category_url_list = scrape_select_categories(url,args.categories)
        print(category_url_list)
    else:
        print("Please provide valid arguments. Use --help for more info.")


if __name__ == "__main__":
    main()
