from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time
import Extract_data_function
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    WebDriverException,
    JavascriptException,
    StaleElementReferenceException,
)


def get_page_content(driver):
    """
    Function to return the HTML source code of the currently loaded web page through the driver object.
    :param driver: driver with website url
    :return: page content in text format
    """
    logging.info(f"Fetching page content via {driver}")
    return driver.page_source


def scroll_to_bottom(driver):
    """
    Function to go to bottom of website.
    :param driver: driver with url for each category site
    :return: None
    """

    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    time.sleep(0.8)


def login(driver, username, password, config):
    """
    Log in to the website using the provided credentials.
    :param driver: The Selenium WebDriver instance.
    :param username: The username for login.
    :param password: The password for login.
    :param config: Configuration dictionary containing messages and settings.
    :return: None
    """

    try:
        signin_button = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//a[text()="Sign In"]')))
        # signin_button = driver.find_element(By.XPATH, '//a[text()="Sign In"]')
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
    except NoSuchElementException as e:
        logging.error(f"Element not found: {e}")
    except TimeoutException as e:
        logging.error(f"Timed out waiting for element: {e}")
    except ElementClickInterceptedException as e:
        logging.error(f"Error clicking element: {e}")
    except ElementNotInteractableException as e:
        logging.error(f"Element not interactable: {e}")
    except WebDriverException as e:
        logging.error(f"Webdriver error: {e}")
    finally:
        logging.info("Successfully logged in")


def process_category(category_url, username, password, option, config):
    """
    Function to open an url in Selenium and act on it by calling the next function that scrolls through it.
    :param category_url: url of category site (e.g. toys)
    :param username: Propstore username
    :param password: Propstore password
    :param option: The scraping option (live_items, sold_items, all_items).
    :param config: Configuration dictionary containing messages and settings.
    :return: None
    """
    driver = webdriver.Chrome()
    driver.get(category_url)
    return scroll_website(driver, username, password, category_url, option, config)


def scroll_website(driver, username, password, category_url, option, config):
    """
    Function to log in to website, scroll down website as long as possible and extract key information.
    This is executed by calling other functions.
    :param driver: driver with url for each category site
    :param username: Propstore username
    :param password: Propstore password
    :param category_url: url of category site (e.g. toys)
    :return: None
    """

    try:
        login(driver, username, password, config)
        logging.info(f"Ran function {login(driver, username, password, config)}")
        time.sleep(2)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            scroll_to_bottom(driver)
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        html_content = get_page_content(driver)
        return Extract_data_function.extract_data(html_content, category_url, option, config)
    except TimeoutException as e:
        logging.error(f"Timeout occurred: {e}")
        return e
    except NoSuchElementException as e:
        logging.error(f"Element not found: {e}")
        return e
    except StaleElementReferenceException as e:
        logging.error(f"Stale element reference: {e}")
        return e
    except JavascriptException as e:
        logging.error(f"JavaScript execution error: {e}")
        return e
    except WebDriverException as e:
        logging.error(f"WebDriver error: {e}")
        return e
    finally:
        driver.quit()
