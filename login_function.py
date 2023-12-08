from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import logging


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
        WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//a[text()="Sign In"]')))
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
    except Exception as error:
        logging.info(config["error_in_login"])
        print(config["error_in_login"])
