"""Page Object страницы Text Input (задание 1).

Сайт: http://uitestingplayground.com/textinput
Сценарий: ввод текста в поле, клик по синей кнопке и проверка того,
что подпись кнопки изменилась на введённый текст.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By

from .base_page import BasePage


class TextInputPage(BasePage):
    """Страница проверки изменения текста кнопки."""

    url = "http://uitestingplayground.com/textinput"

    _INPUT = (By.ID, "newButtonName")
    _BUTTON = (By.ID, "updatingButton")

    def enter_button_name(self, text: str) -> "TextInputPage":
        """Вводит новое имя кнопки в текстовое поле.

        Args:
            text: текст, который станет подписью кнопки после клика.

        Returns:
            Сам объект страницы для цепочки вызовов.
        """
        field = self.find_visible(self._INPUT)
        field.clear()
        field.send_keys(text)
        return self

    def click_button(self) -> "TextInputPage":
        """Кликает по синей кнопке, обновляющей свою подпись.

        Returns:
            Сам объект страницы для цепочки вызовов.
        """
        self.find_clickable(self._BUTTON).click()
        return self

    def get_button_text(self) -> str:
        """Возвращает текущую подпись кнопки.

        Returns:
            Видимый текст кнопки.
        """
        return self.find_visible(self._BUTTON).text
