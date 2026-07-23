"""Задание 2: проверка загрузки изображений и атрибута alt."""

from selenium.webdriver.chrome.webdriver import WebDriver

from pages.loading_images_page import LoadingImagesPage

THIRD_IMAGE_INDEX = 2
EXPECTED_ALT = "award"


def test_third_image_alt_is_award(driver: WebDriver) -> None:
    """Атрибут alt третьего изображения равен "award".

    Шаги:
        1. Открыть страницу Loading Images.
        2. Дождаться загрузки всех изображений.
        3. Получить атрибут alt третьего изображения.
        4. Проверить, что он равен "award".
    """
    page = LoadingImagesPage(driver).open()
    page.wait_all_images_loaded()

    alt = page.get_image_alt(THIRD_IMAGE_INDEX)
    assert alt == EXPECTED_ALT, (
        f"Ожидался alt '{EXPECTED_ALT}', получен '{alt}'"
    )
