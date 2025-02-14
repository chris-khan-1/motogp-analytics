import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def setup_chrome_driver() -> webdriver.Chrome:
    """Setup Chrome WebDriver with headless mode."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    chrome_options.add_argument("--disable-usb")

    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)


def select_element_by_value(
    driver: webdriver.Chrome, selector: str, value: str
) -> None:
    """Select the element from the dropdown."""

    WebDriverWait(driver=driver, timeout=10).until(
        method=EC.presence_of_element_located(locator=(By.CSS_SELECTOR, selector))
    )

    element = driver.find_element(
        by=By.CSS_SELECTOR,
        value=selector,
    )
    dropdown = Select(webelement=element)
    dropdown.select_by_value(value=value)


def extract_event_data(driver: webdriver.Chrome) -> list[dict]:
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


def get_event_data_for_year(year: str) -> list[dict]:
    """Get event data for a given year."""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name=__name__)

    try:
        driver = setup_chrome_driver()
        logger.info("Chrome WebDriver initialised.")

        driver.get(url="https://www.motogp.com/en/gp-results")
        logger.info("Navigated to MotoGP results page.")

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

        logger.info(f"Selected year: {year} and event type: GP.")

        events_data = extract_event_data(driver=driver)
        logger.info("Event data extracted successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        events_data = []

    finally:
        driver.quit()
        logger.info("Browser closed.")

    return events_data
