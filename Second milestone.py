from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import json



def read_config():
    """function to read json configuration file"""
    with open("config.json", "r") as json_file:
        json_dict = json.load(json_file)
    return json_dict


def get_page_content(driver):
    """function to download all movie content in text format"""
    return driver.page_source


def extract_data(html_content, category_url):
    """function to extract movie name, sale date and price (either sold or offer if live) from website"""
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
            # print(f"Movie: {movie_name}, Title: {card_title}, Price: {price}")
        except Exception as error:
            print(f"error {error}")
            continue
    print(card_dict)


def can_scroll(driver):
    """function to check that website can be scrolled down further"""
    return driver.execute_script(
        "return window.scrollY + window.innerHeight < document.body.scrollHeight;")  # scroll down completely body


def scroll_to_bottom(driver):
    """function to scroll down website"""
    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    time.sleep(1)


def scroll_website(driver, username, password,category_url):
    """function to check if we can scroll down further on website (via can_scroll function) and if True, scroll down website (via scroll_to_bottom function). Next
     get all prop data from get_page_content function and then take relevant info via extract_data function before quitting"""
    login(driver, username, password)
    time.sleep(3)
    try:
        i = 0
        while can_scroll(driver) and i < 3:
            scroll_to_bottom(driver)
            html_content = get_page_content(driver)
            extract_data(html_content,category_url)
            WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, "body")))
            i += 1
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


def login(driver, username, password):
    """function to log in to website """

    signin_button = driver.find_element(By.XPATH, '//a[text()="Sign In"]')
    signin_button.click()

    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//input[@id="email"]')))
    username_field = driver.find_element(By.XPATH, '//input[@id="email"]')
    username_field.send_keys(username)
    password_field = driver.find_element(By.XPATH, '//input[@id="password"]')
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 30).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'button.modal-register__submit')))
    login_button.click()
    WebDriverWait(driver, 10)

def go_through_categories(url):
    """docstring placeholder"""
    category_list = ["props", "costumes", "artwork", "posters", "toys", "autographs", "promotional-items"]
    category_url_list = [url.replace("products", f"category/{category}") for category in category_list]
    return category_url_list


def main():
    """main function to run through propstore.com, scroll to the bottom of the page and take movie information"""
    config = read_config()
    url = config["url"]
    username = config["username"]
    password = config["password"]

    category_url_list = go_through_categories(url)
    for category_url in category_url_list:
        driver = webdriver.Chrome()
        driver.get(category_url)
        scroll_website(driver, username, password, category_url)


if __name__ == "__main__":
    main()
