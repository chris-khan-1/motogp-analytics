from unittest.mock import MagicMock, patch

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from app.utils.web_scraping import (
    select_element_by_value,
    setup_chrome_driver,
)


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

    mock_driver_instance = MagicMock(spec=WebDriver)
    mock_chrome_class.return_value = mock_driver_instance

    driver = setup_chrome_driver()

    actual_options = mock_chrome_class.call_args[1]["options"]

    assert driver == mock_driver_instance

    assert set(actual_options.arguments) == expected_chrome_arguments


class TestSelectElementByValue:
    @pytest.fixture(scope="class")
    def mock_driver(self):
        driver = MagicMock()
        driver.find_element.return_value = MagicMock()
        return driver

    @patch(target="app.utils.web_scraping.Select")
    @patch(target="app.utils.web_scraping.WebDriverWait")
    def test_successful_selection(
        self, mock_wait_class, mock_select_class, mock_driver: MagicMock
    ):
        mock_select = MagicMock(spec=Select)
        mock_element = MagicMock()
        mock_wait = MagicMock()

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

    @patch("app.utils.web_scraping.WebDriverWait")
    def test_no_element_timeout_scenario(self, mock_wait, mock_driver: MagicMock):
        mock_wait.return_value.until.side_effect = TimeoutException()

        with pytest.raises(TimeoutException):
            select_element_by_value(
                driver=mock_driver, selector="test-selector", value="test-value"
            )


# class TestExtractEventData:
#     @pytest.fixture
#     def mock_driver(self):
#         return MagicMock()

#     def test_successful_extraction(self, mock_driver):
#         mock_option = MagicMock()
#         mock_option.get_attribute.side_effect = ["Event 1", "value1"]
#         mock_option.text = "Displayed Text 1"

#         mock_select = MagicMock()
#         mock_select.options = [mock_option]

#         mock_driver.find_element.return_value = mock_select

#         result = extract_event_data(mock_driver)

#         assert len(result) == 1
#         assert result[0]["name"] == "Event 1"
#         assert result[0]["value"] == "value1"
#         assert result[0]["displayed_text"] == "Displayed Text 1"


#     def test_empty_options(self, mock_driver):
#         mock_select = MagicMock()
#         mock_select.options = []
#         mock_driver.find_element.return_value = mock_select

#         result = extract_event_data(mock_driver)

#         assert len(result) == 0


# class TestGetEventDataForYear:
#     @patch("app.utils.web_scraping.setup_chrome_driver")
#     @patch("app.utils.web_scraping.select_element_by_value")
#     @patch("app.utils.web_scraping.extract_event_data")
#     def test_successful_data_retrieval(self, mock_extract, mock_select, mock_setup):
#         mock_driver = MagicMock()
#         mock_setup.return_value = mock_driver
#         mock_extract.return_value = [{"name": "Test Event"}]

#         result = get_event_data_for_year("2023")

#         assert len(result) == 1
#         assert result[0]["name"] == "Test Event"
#         mock_driver.quit.assert_called_once()

#     @patch("app.utils.web_scraping.setup_chrome_driver")
#     def test_error_handling(self, mock_setup):
#         mock_setup.side_effect = Exception("Test error")

#         result = get_event_data_for_year("2023")

#         assert result == []

#     @patch("app.utils.web_scraping.setup_chrome_driver")
#     @patch("app.utils.web_scraping.logging")
#     def test_logging(self, mock_logging, mock_setup):
#         mock_driver = MagicMock()
#         mock_setup.return_value = mock_driver

#         get_event_data_for_year("2023")

#         mock_logging.getLogger.assert_called_once()
#         mock_logging.basicConfig.assert_called_once_with(level=mock_logging.INFO)
