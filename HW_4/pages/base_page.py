"""Базовый Page Object с общими действиями над страницей.

Инкапсулирует работу с WebDriver и явными ожиданиями, чтобы страницы-
наследники не дублировали низкоуровневый код (принципы DRY и SRP).
Расширять поведение следует наследованием, не изменяя базовый класс
(принцип OCP из SOLID).
"""

from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

Locator = tuple[str, str]

DEFAULT_TIMEOUT = 15


class BasePage:
    """Общий предок всех Page Object-ов.

    Attributes:
        driver: активный экземпляр WebDriver.
        timeout: время ожидания элементов по умолчанию, секунды.
    """

    #: URL страницы; переопределяется в наследниках.
    url: str = ""

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Сохраняет драйвер и настраивает таймаут ожиданий.

        Args:
            driver: активный экземпляр WebDriver.
            timeout: время ожидания элементов по умолчанию, секунды.
        """
        self.driver = driver
        self.timeout = timeout
        self._wait = WebDriverWait(driver, timeout)

    def open(self) -> BasePage:
        """Открывает страницу по её URL.

        Returns:
            Сам объект страницы для цепочки вызовов.
        """
        self.driver.get(self.url)
        return self

    def find_visible(self, locator: Locator) -> WebElement:
        """Ждёт и возвращает видимый элемент по локатору.

        Args:
            locator: пара (By, значение).

        Returns:
            Видимый элемент.

        Raises:
            TimeoutException: если элемент не появился за timeout секунд.
        """
        return self._wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator: Locator) -> WebElement:
        """Ждёт и возвращает кликабельный элемент по локатору.

        Args:
            locator: пара (By, значение).

        Returns:
            Кликабельный элемент.

        Raises:
            TimeoutException: если элемент не стал кликабельным за timeout.
        """
        return self._wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator: Locator) -> list[WebElement]:
        """Ждёт появления хотя бы одного элемента и возвращает все совпадения.

        Args:
            locator: пара (By, значение).

        Returns:
            Список найденных элементов.

        Raises:
            TimeoutException: если ни один элемент не появился за timeout.
        """
        return self._wait.until(
            EC.presence_of_all_elements_located(locator)
        )
