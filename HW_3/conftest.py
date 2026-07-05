"""Фикстуры Pytest для UI-тестов itcareerhub.de."""

from collections.abc import Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    """Создаёт и отдаёт экземпляр Chrome WebDriver.

    Драйвер настроен на максимизацию окна и неявное ожидание.
    После теста браузер закрывается в любом случае.

    Yields:
        WebDriver: готовый к работе экземпляр Chrome.
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    # Раскомментировать для запуска без графического окна (CI):
    # options.add_argument("--headless=new")
    # options.add_argument("--window-size=1920,1080")

    chrome = webdriver.Chrome(options=options)
    chrome.implicitly_wait(5)
    try:
        yield chrome
    finally:
        chrome.quit()
