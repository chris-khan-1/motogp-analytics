import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from app.web_scraping.utils import select_element_by_value, setup_chrome_driver


def extract_event_data(driver: webdriver.Chrome) -> list[dict[str, str | int | None]]:
    """Extract event data from the event dropdown."""

    event_type_selector = driver.find_element(
        by=By.CSS_SELECTOR,
        value=".primary-filter__filter-select.primary-filter__filter-select--event",
    )
    event_dropdown = Select(webelement=event_type_selector)

    WebDriverWait(driver=driver, timeout=10).until(
        method=EC.presence_of_all_elements_located(
            locator=(
                By.CSS_SELECTOR,
                (
                    ".primary-filter__filter-select.primary-filter__filter-select--event"
                    " option"
                ),
            )
        )
    )

    events_data = []
    for i, option in enumerate(event_dropdown.options[::-1]):  # reverse option order
        event = {
            "round": i + 1,
            "name": option.get_attribute("name"),
            "url_value": option.get_attribute("value"),
            "displayed_text": option.text,
        }
        events_data.append(event)

    return events_data


def get_event_data_for_year(year: str) -> list[dict[str, str | int | None]]:
    """Get event data for a given year."""

    driver = setup_chrome_driver()
    logging.info("Chrome WebDriver initialised.")

    driver.get(url="https://www.motogp.com/en/gp-results")
    logging.info("Navigated to MotoGP results page.")

    # select year
    select_element_by_value(
        driver=driver, selector=".primary-filter__filter-select--year", value=year
    )

    # select GP event type
    select_element_by_value(
        driver=driver,
        selector=".primary-filter__filter-select.primary-filter__filter-select--type",
        value="GP",
    )

    logging.info(f"Selected year: {year} and event type: GP.")

    events_data = extract_event_data(driver=driver)
    logging.info("Event data extracted successfully.")

    driver.quit()
    logging.info("Browser closed.")

    return events_data
