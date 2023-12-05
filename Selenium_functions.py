from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time
import Extract_data_function

def can_scroll(driver):
    """
    function to check that website can be scrolled down further
    :param driver:
    :return:
    """

    return driver.execute_script(
        "return window.scrollY + window.innerHeight < document.body.scrollHeight;")  # scroll down completely body
def get_page_content(driver):
    """

    :param driver: driver with website url
    :return: page content in text format
    """
    logging.info(f"Fetching page content via {driver}")
    return driver.page_source
def scroll_to_bottom(driver):
    """
    function to scroll down website
    :param driver:
    :return:
    """

    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    time.sleep(1)


def login(driver, username, password):
    """
    function to log in to website
    :param driver:
    :param username:
    :param password:
    :return:
    """

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

def process_category(category_url, username, password):
    """
    [PLACEHOLDER]
    :param category_url:
    :param username:
    :param password:
    :return:
    """
    driver = webdriver.Chrome()
    driver.get(category_url)
    scroll_website(driver, username, password, category_url)


def scroll_website(driver, username, password, category_url):
    """
    function to check if we can scroll down further on website (via can_scroll function) and if True, scroll down website (via scroll_to_bottom function). Next
    get all prop data from get_page_content function and then take relevant info via extract_data function before quitting
    :param driver:
    :param username:
    :param password:
    :param category_url:
    :return:
    """

    login(driver, username, password)
    logging.info(f"Ran function {login(driver, username, password)}")
    time.sleep(3)
    try:
        i = 0
        while can_scroll(driver) and i < 3:
            scroll_to_bottom(driver)
            html_content = get_page_content(driver)
            Extract_data_function.extract_data(html_content, category_url)
            WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.TAG_NAME, "body")))
            i += 1
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()