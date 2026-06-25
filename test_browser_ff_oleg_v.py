from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_payment(driver):
    driver.get("https://itcareerhub.de/ru")
    sleep(2)
    about_link = driver.find_element(By.LINK_TEXT, "Способы оплаты")
    about_link.click()
    sleep(2)
    driver.save_screenshot("./hw_2_screen.png")
