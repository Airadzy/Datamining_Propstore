from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

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