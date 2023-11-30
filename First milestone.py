from bs4 import BeautifulSoup
import time
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
    """function to download all movie content"""
    return driver.page_source


def extract_data(html_content):
    """function to extract movie name, sale date and price (either sold or offer if live) from website"""

    soup = BeautifulSoup(html_content, "html.parser")
    for item_tag in soup.find_all(["div", "span"], class_=["card__movie", "card__price-soldon",
                                                           "card__price-title"]):  # TODO update based on categories and show date sold on if archive sale
        item_content = item_tag.text.strip()
        print(item_content, end="\n")  # Print on the same line


def can_scroll(driver):
    """function to check that website can be scrolled down further"""
    return driver.execute_script(
        "return window.scrollY + window.innerHeight < document.body.scrollHeight;")  # scroll down completely body


def scroll_to_bottom(driver):
    """function to scroll down website"""
    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    time.sleep(1)


def login(driver, username, password):  # TODO update login method
    """function to login to website (IN CONSTRUCTION)"""
    pass
    # signin_button = driver.find_element(By.XPATH, '//a[text()="Sign In"]')
    # signin_button.click()
    #
    # username_field = driver.find_element(By.ID,"email")
    # username_field.send_keys(username)
    #
    # password_field = driver.find_element(By.ID,"password")
    # password_field.send_keys(password)
    #
    # login_button = driver.find_element(By.ID,"Submit")


def scroll_website(driver):
    """function to check if we can scroll down further on website (via can_scroll function) and if True, scroll down website (via scroll_to_bottom function). Next
     get all prop data from get_page_content function and then take relevant info via extract_data function before quitting"""
    login(driver, "a.radzyminski@icloud.com", "xxx")  # TODO: update login method
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
    """main function to run through propstore.com, scroll to the bottom of the page and take movie information"""
    url = "https://propstore.com/products/?sortType=5&buyNow=1&archive=1&scroll=220"
    driver = webdriver.Chrome()  # initialize webbrowser (Chrome in this instance)
    driver.get(url)
    scroll_website(driver)
    # soup = download_archive(url)
    # links = extract_data(soup)


if __name__ == "__main__":
    main()
