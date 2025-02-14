from unittest.mock import MagicMock, call, patch

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from app.utils.web_scraping import (
    extract_event_data,
    get_event_data_for_year,
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


class TestExtractEventData:
    @pytest.fixture
    def mock_driver(self):
        return MagicMock()

    @patch("app.utils.web_scraping.Select")
    def test_extract_event_data_successful_extraction(
        self, mock_select_class, mock_driver
    ):
        mock_option1 = MagicMock()
        mock_option1.get_attribute.side_effect = ["Event 1", "value1"]
        mock_option1.text = "Text 1"

        mock_option2 = MagicMock()
        mock_option2.get_attribute.side_effect = ["Event 2", "value2"]
        mock_option2.text = "Text 2"

        mock_select = mock_select_class.return_value
        mock_select.options = [mock_option2, mock_option1]  # reverse order

        mock_driver.find_element.return_value = MagicMock()

        actual = extract_event_data(driver=mock_driver)

        mock_driver.find_element.assert_called_once_with(
            by=By.CSS_SELECTOR,
            value=".primary-filter__filter-select.primary-filter__filter-select--event",
        )

        expected = [
            {
                "round": 1,
                "name": "Event 1",
                "url_value": "value1",
                "displayed_text": "Text 1",
            },
            {
                "round": 2,
                "name": "Event 2",
                "url_value": "value2",
                "displayed_text": "Text 2",
            },
        ]

        assert actual == expected

    @patch("app.utils.web_scraping.Select")
    def test_extract_event_data_empty_options(self, mock_select_class, mock_driver):  # noqa: ARG002
        mock_select = MagicMock()
        mock_select.options = []
        mock_driver.find_element.return_value = mock_select

        result = extract_event_data(driver=mock_driver)

        assert len(result) == 0

    @patch("app.utils.web_scraping.Select")
    @patch("app.utils.web_scraping.WebDriverWait")
    def test_extract_event_data_timeout_exception(
        self,
        mock_wait_class,
        mock_select_class,  # noqa: ARG002
        mock_driver,
    ):
        mock_wait = mock_wait_class.return_value
        mock_wait.until.side_effect = TimeoutException("Timeout waiting for options")

        with pytest.raises(TimeoutException):
            extract_event_data(driver=mock_driver)


class TestGetEventDataForYear:
    @patch("app.utils.web_scraping.setup_chrome_driver")
    @patch("app.utils.web_scraping.select_element_by_value")
    @patch("app.utils.web_scraping.extract_event_data")
    def test_get_event_data_for_year_successful_execution(
        self,
        mock_extract_event_data,
        mock_select_element_by_value,
        mock_setup_chrome_driver,
    ):
        mock_driver = MagicMock()
        mock_setup_chrome_driver.return_value = mock_driver

        # invoking the function here
        get_event_data_for_year(year="2023")

        mock_setup_chrome_driver.assert_called_once()

        mock_driver.get.assert_called_once_with(
            url="https://www.motogp.com/en/gp-results"
        )

        mock_select_element_by_value.assert_has_calls(
            [
                call(
                    driver=mock_driver,
                    selector=".primary-filter__filter-select--year",
                    value="2023",
                ),
                call(
                    driver=mock_driver,
                    selector=".primary-filter__filter-select.primary-filter__filter-select--type",
                    value="GP",
                ),
            ],
        )

        mock_extract_event_data.assert_called_once_with(driver=mock_driver)

        mock_driver.quit.assert_called_once()
