"""Фикстуры Pytest для UI-тестов HW_4."""

from collections.abc import Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    """Создаёт и отдаёт экземпляр Chrome WebDriver.

    Драйвер максимизирует окно; после теста браузер закрывается всегда.

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
    try:
        yield chrome
    finally:
        chrome.quit()
