"""Автотесты главной страницы https://itcareerhub.de/ru.

Стратегия локаторов: элементы находятся через CSS-селекторы
(By.CSS_SELECTOR), а текстовые проверки выполняются в Python через
element.text — так как CSS не поддерживает поиск по тексту узла.
"""

import time

import pytest
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

BASE_URL = "https://itcareerhub.de/ru"
TIMEOUT = 15

# Демо-паузы для наглядности прогона. В реальных тестах не нужны —
# достаточно явных ожиданий. Установить 0, чтобы отключить.
DEMO_PAUSE = 2

# CSS-селекторы структурных элементов.
LOGO_CSS = "img[alt*='Career']"
COOKIE_BUTTON_CSS = ".t-cookie__button, [class*='cookie'] button, .t390 button"
POPUP_CSS = ".t-popup, [class*='popup'], [class*='modal']"

# Тексты пунктов меню шапки (сравниваются с element.text).
HEADER_LINKS = [
    "Программы",
    "Способы оплаты",
    "О нас",
    "Отзывы",
    "Блог",
]

CALLBACK_TEXT = "Обратный звонок"
POPUP_TEXT = "Запишитесь на бесплатную карьерную консультацию"


def _norm(value: str) -> str:
    """Нормализует текст для сравнения: убирает лишние пробелы и регистр.

    Selenium возвращает element.text как отрендеренный текст, включая
    CSS text-transform (например, uppercase), поэтому сравнение должно
    быть регистронезависимым.

    Args:
        value: исходная строка.

    Returns:
        Строка без повторяющихся пробелов, приведённая к нижнему регистру.
    """
    return " ".join(value.split()).casefold()


def _find_visible_link(driver: WebDriver, text: str) -> WebElement | None:
    """Ищет видимую ссылку <a> с точным текстом.

    Собирает все ссылки CSS-селектором и фильтрует по тексту в Python,
    поскольку CSS не умеет искать по содержимому узла.

    Args:
        driver: активный экземпляр WebDriver.
        text: точный видимый текст ссылки.

    Returns:
        Найденный видимый элемент или None, если совпадений нет.
    """
    for anchor in driver.find_elements(By.CSS_SELECTOR, "a"):
        if _norm(anchor.text) == _norm(text) and anchor.is_displayed():
            return anchor
    return None


def _find_visible_clickable(driver: WebDriver, text: str) -> WebElement | None:
    """Ищет видимый кликабельный элемент (a или button), содержащий текст.

    Args:
        driver: активный экземпляр WebDriver.
        text: искомая подстрока текста элемента.

    Returns:
        Найденный видимый элемент или None.
    """
    for element in driver.find_elements(By.CSS_SELECTOR, "a, button"):
        if _norm(text) in _norm(element.text) and element.is_displayed():
            return element
    return None


def _find_visible_popup_with_text(
    driver: WebDriver, text: str
) -> WebElement | None:
    """Ищет видимый попап/модальное окно, содержащее указанный текст.

    Args:
        driver: активный экземпляр WebDriver.
        text: искомая подстрока текста внутри попапа.

    Returns:
        Видимый контейнер попапа с текстом или None.
    """
    for container in driver.find_elements(By.CSS_SELECTOR, POPUP_CSS):
        if container.is_displayed() and _norm(text) in _norm(container.text):
            return container
    return None


def _wait_visible_link(driver: WebDriver, text: str) -> WebElement:
    """Ждёт появления видимой ссылки с заданным текстом.

    Args:
        driver: активный экземпляр WebDriver.
        text: точный видимый текст ссылки.

    Returns:
        Дождавшийся видимый элемент.

    Raises:
        TimeoutException: если ссылка не появилась за TIMEOUT секунд.
    """
    return WebDriverWait(driver, TIMEOUT).until(
        lambda d: _find_visible_link(d, text)
    )


def _accept_cookies(driver: WebDriver) -> None:
    """Закрывает cookie-баннер, если он присутствует.

    Баннер перехватывает клики, поэтому убирается до основных действий.
    Отсутствие баннера ошибкой не считается.

    Args:
        driver: активный экземпляр WebDriver.
    """
    try:
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, COOKIE_BUTTON_CSS))
        )
        button.click()
    except TimeoutException:
        pass


@pytest.fixture
def open_main_page(driver: WebDriver) -> WebDriver:
    """Открывает главную страницу и закрывает cookie-баннер.

    Args:
        driver: активный экземпляр WebDriver.

    Returns:
        Драйвер на открытой главной странице.
    """
    driver.get(BASE_URL)
    _accept_cookies(driver)
    return driver


def test_logo_is_displayed(open_main_page: WebDriver) -> None:
    """Логотип ITCareerHub отображается в шапке страницы."""
    driver = open_main_page
    logo = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, LOGO_CSS))
    )
    assert logo.is_displayed(), "Логотип ITCareerHub не отображается"


@pytest.mark.parametrize("link_text", HEADER_LINKS)
def test_header_link_is_displayed(
    open_main_page: WebDriver, link_text: str
) -> None:
    """Каждая ссылка меню шапки отображается на странице.

    Args:
        open_main_page: драйвер на открытой главной странице.
        link_text: текст проверяемой ссылки.
    """
    element = _find_visible_link(open_main_page, link_text)
    assert element is not None, f"Ссылка '{link_text}' не отображается"


def test_language_switchers_are_displayed(open_main_page: WebDriver) -> None:
    """Переключатели языка ru и de присутствуют и видимы."""
    driver = open_main_page
    assert _find_visible_link(driver, "ru") is not None, (
        "Переключатель 'ru' не найден"
    )
    assert _find_visible_link(driver, "de") is not None, (
        "Переключатель 'de' не найден"
    )


def test_contacts_link_is_available(open_main_page: WebDriver) -> None:
    """Ссылка «Контакты» доступна в подменю «О нас».

    Пункт «Контакты» скрыт в выпадающем подменю «О нас», поэтому
    сначала наводим курсор на «О нас», затем проверяем видимость.
    """
    driver = open_main_page
    about = _wait_visible_link(driver, "О нас")
    ActionChains(driver).move_to_element(about).perform()

    contacts = _wait_visible_link(driver, "Контакты")
    assert contacts.is_displayed(), "Ссылка 'Контакты' не отображается"


def test_callback_popup_appears(open_main_page: WebDriver) -> None:
    """Полный сценарий: переход в «Контакты» и обратный звонок.

    Кликает «Контакты», затем «Обратный звонок» и проверяет, что во
    всплывающем окне появляется ожидаемый текст консультации.
    """
    driver = open_main_page

    # 1. Открываем подменю «О нас» и кликаем «Контакты».
    about = _wait_visible_link(driver, "О нас")
    ActionChains(driver).move_to_element(about).perform()
    time.sleep(DEMO_PAUSE)  # демо: видно раскрытие подменю
    contacts = _wait_visible_link(driver, "Контакты")
    contacts.click()

    _accept_cookies(driver)
    time.sleep(DEMO_PAUSE)  # демо: видно загрузку страницы контактов

    # 2. Кликаем кнопку «Обратный звонок».
    callback = WebDriverWait(driver, TIMEOUT).until(
        lambda d: _find_visible_clickable(d, CALLBACK_TEXT)
    )
    try:
        callback.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", callback)
    time.sleep(DEMO_PAUSE)  # демо: видно открытие всплывающего окна

    # 3. Проверяем текст во всплывающем окне.
    popup = WebDriverWait(driver, TIMEOUT).until(
        lambda d: _find_visible_popup_with_text(d, POPUP_TEXT)
    )
    assert popup is not None, (
        f"Текст '{POPUP_TEXT}' не отображается во всплывающем окне"
    )
    time.sleep(DEMO_PAUSE)  # демо: видно итоговое окно перед закрытием