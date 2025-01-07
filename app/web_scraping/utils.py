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
