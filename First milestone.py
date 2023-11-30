from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


def get_page_content(driver):
    """docstring placeholder"""
    return driver.page_source


def extract_data(html_content):
    """docstring placeholder"""
    soup = BeautifulSoup(html_content, "html.parser")

    # movie reference: <div class="card__movie" title="STAR TREK: ENTERPRISE (2001-2005)">STAR TREK: ENTERPRISE (2001-2005)"
    # sold on: <span class="card__price-soldon">Sold on 3 Nov, 2023</span>
    # <span class="card__price-title">$695</span>
    for item_tag in soup.findAll("div", class_="card__movie"):
        item_reference = item_tag.get("title")
        print(f"Movie URL: {item_reference}\n")

    for sold_on in soup.findAll("span", class_="card__price-soldon"):
        sold_date = sold_on.text.strip(" ")
        print(f"sold date: {sold_date}")

    for price_tag in soup.findAll("span", class_="card__price-title"):
        price = price_tag.text.strip(" ")
        print(f"price tag: {price}")


def can_scroll(driver):
    """function to check that website can be scrolled down further"""
    return driver.execute_script(
        "return window.scrollY + window.innerHeight < document.body.scrollHeight;")  # scroll down completely body


def scroll_to_bottom(driver):
    """function to scroll down website"""
    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    time.sleep(1)


def scroll_website(driver):
    try:
        while can_scroll(driver):
            scroll_to_bottom(driver)
            html_content = get_page_content(driver)
            extract_data(html_content)
            WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, "body")))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        time.sleep(10)
        driver.quit()


def main():
    """main function"""
    url = "https://propstore.com/products/?auction=1&buyNow=1&archive=1"
    driver = webdriver.Chrome()  # initialize webbrowser (Chrome in this instance)
    driver.get(url)
    scroll_website(driver)
    # soup = download_archive(url)
    # links = extract_data(soup)


if __name__ == "__main__":
    main()
