"""Page Object страницы Loading Images (задание 2).

Сайт: https://bonigarcia.dev/selenium-webdriver-java/loading-images.html
Сценарий: дождаться загрузки всех изображений и получить атрибут alt
третьего изображения.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from .base_page import BasePage


class LoadingImagesPage(BasePage):
    """Страница проверки загрузки изображений."""

    url = (
        "https://bonigarcia.dev/selenium-webdriver-java/loading-images.html"
    )

    #: Изображения появляются в контейнере по мере загрузки.
    _IMAGES = (By.CSS_SELECTOR, "#image-container img")
    #: Ожидаемое итоговое количество изображений на странице.
    _EXPECTED_COUNT = 3

    def wait_all_images_loaded(self) -> "LoadingImagesPage":
        """Ждёт, пока все изображения появятся и полностью прогрузятся.

        Сначала дожидается ожидаемого числа элементов <img>, затем через
        свойство complete проверяет, что каждое изображение догрузилось.

        Returns:
            Сам объект страницы для цепочки вызовов.
        """
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: len(d.find_elements(*self._IMAGES))
            >= self._EXPECTED_COUNT
        )
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: all(
                d.execute_script("return arguments[0].complete;", img)
                for img in d.find_elements(*self._IMAGES)
            )
        )
        return self

    def get_image(self, index: int) -> WebElement:
        """Возвращает изображение по его порядковому номеру (с нуля).

        Args:
            index: индекс изображения в списке, начиная с 0.

        Returns:
            Элемент изображения.
        """
        return self.find_all(self._IMAGES)[index]

    def get_image_alt(self, index: int) -> str:
        """Возвращает значение атрибута alt изображения по индексу.

        Args:
            index: индекс изображения в списке, начиная с 0.

        Returns:
            Значение атрибута alt.
        """
        return self.get_image(index).get_attribute("alt")
