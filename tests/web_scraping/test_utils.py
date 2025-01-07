from unittest.mock import Mock, patch

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from app.web_scraping.utils import (
    select_element_by_value,
    setup_chrome_driver,
)

_PATH_BASE_PATH = "app.web_scraping.utils"


@patch("selenium.webdriver.Chrome")
def test_setup_chrome_driver_correct_options(mock_chrome_class):
    expected_chrome_arguments = {
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--enable-unsafe-swiftshader",
        "--disable-usb",
    }

    mock_driver_instance = Mock(spec=WebDriver)
    mock_chrome_class.return_value = mock_driver_instance

    driver = setup_chrome_driver()

    actual_options = mock_chrome_class.call_args[1]["options"]

    assert driver == mock_driver_instance

    assert set(actual_options.arguments) == expected_chrome_arguments


class TestSelectElementByValue:
    @pytest.fixture(scope="class")
    def mock_driver(self):
        driver = Mock()
        driver.find_element.return_value = Mock()
        return driver

    @patch(target="app.web_scraping.utils.Select")
    @patch(target="app.web_scraping.utils.WebDriverWait")
    def test_successful_selection(
        self, mock_wait_class, mock_select_class, mock_driver
    ):
        mock_select = Mock(spec=Select)
        mock_element = Mock()
        mock_wait = Mock()

        mock_driver.find_element.return_value = mock_element
        mock_wait.until.return_value = mock_element
        mock_select_class.return_value = mock_select
        mock_wait_class.return_value = mock_wait

        select_element_by_value(
            driver=mock_driver, selector="test-selector", value="test-value"
        )

        mock_wait_class.assert_called_once_with(driver=mock_driver, timeout=10)

        mock_wait.until.assert_called_once()

        mock_driver.find_element.assert_called_once_with(
            by=By.CSS_SELECTOR, value="test-selector"
        )

        mock_select_class.assert_called_once_with(webelement=mock_element)

        mock_select.select_by_value.assert_called_once_with(value="test-value")

    @patch(f"{_PATH_BASE_PATH}.WebDriverWait")
    def test_no_element_timeout_scenario(self, mock_wait, mock_driver):
        mock_wait.return_value.until.side_effect = TimeoutException()

        with pytest.raises(TimeoutException):
            select_element_by_value(
                driver=mock_driver, selector="test-selector", value="test-value"
            )
