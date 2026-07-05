from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep
import pytest

@pytest.fixture()
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_data(driver):
    driver.get('https://the-internet.herokuapp.com/login')
    first_field = driver.find_element(By.ID, 'username')
    first_field.send_keys('tomsmith')
    # sleep(1)
    second_field = driver.find_element(By.ID, 'password')
    second_field.send_keys('SuperSecretPassword!')
    login_button = driver.find_element(By.XPATH, '//*[@id="login"]/button')
    login_button.click()
    element = driver.find_element(By.XPATH, '//div[@data-alert="" and @id="flash" and @class="flash success"]')
    print(element.text)
    assert driver.current_url == "https://the-internet.herokuapp.com/secure"
    assert "You logged into a secure area!\n×" == element.text
    # sleep(1)