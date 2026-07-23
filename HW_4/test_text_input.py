"""Задание 1: проверка изменения текста кнопки на Text Input."""

from selenium.webdriver.chrome.webdriver import WebDriver

from pages.text_input_page import TextInputPage

BUTTON_NAME = "ITCH"


def test_button_text_changes_to_input(driver: WebDriver) -> None:
    """Подпись кнопки меняется на введённый в поле текст.

    Шаги:
        1. Открыть страницу Text Input.
        2. Ввести в поле текст "ITCH".
        3. Нажать синюю кнопку.
        4. Проверить, что текст кнопки стал "ITCH".
    """
    page = TextInputPage(driver).open()
    page.enter_button_name(BUTTON_NAME).click_button()

    assert page.get_button_text() == BUTTON_NAME, (
        f"Ожидался текст кнопки '{BUTTON_NAME}', "
        f"получен '{page.get_button_text()}'"
    )
