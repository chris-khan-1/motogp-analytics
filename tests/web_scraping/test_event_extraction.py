from unittest.mock import Mock, call, patch

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from app.web_scraping.event_extraction import (
    extract_event_data,
    get_event_data_for_year,
)

_PATCH_BASE_PATH = "app.web_scraping.event_extraction"


class TestExtractEventData:
    @pytest.fixture
    def mock_driver(self):
        return Mock()

    @patch(f"{_PATCH_BASE_PATH}.Select")
    def test_extract_event_data_successful_extraction(
        self, mock_select_class, mock_driver
    ):
        mock_option1 = Mock()
        mock_option1.get_attribute.side_effect = ["Event 1", "value1"]
        mock_option1.text = "Text 1"

        mock_option2 = Mock()
        mock_option2.get_attribute.side_effect = ["Event 2", "value2"]
        mock_option2.text = "Text 2"

        mock_select = mock_select_class.return_value
        mock_select.options = [mock_option2, mock_option1]  # reverse order

        mock_driver.find_element.return_value = Mock()

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

    @patch(f"{_PATCH_BASE_PATH}.Select")
    def test_extract_event_data_empty_options(self, mock_select, mock_driver):
        mock_select.options = []
        mock_driver.find_element.return_value = mock_select

        actual = extract_event_data(driver=mock_driver)

        assert len(actual) == 0

    @patch(f"{_PATCH_BASE_PATH}.Select", Mock())
    @patch(f"{_PATCH_BASE_PATH}.WebDriverWait")
    def test_extract_event_data_timeout_exception(
        self,
        mock_wait_class,
        mock_driver,
    ):
        mock_wait = mock_wait_class.return_value
        mock_wait.until.side_effect = TimeoutException("Timeout waiting for options")

        with pytest.raises(TimeoutException):
            extract_event_data(driver=mock_driver)


class TestGetEventDataForYear:
    @patch(f"{_PATCH_BASE_PATH}.setup_chrome_driver")
    @patch(f"{_PATCH_BASE_PATH}.select_element_by_value")
    @patch(f"{_PATCH_BASE_PATH}.extract_event_data")
    def test_get_event_data_for_year_successful_execution(
        self,
        mock_extract_event_data,
        mock_select_element_by_value,
        mock_setup_chrome_driver,
    ):
        mock_driver = Mock()
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
