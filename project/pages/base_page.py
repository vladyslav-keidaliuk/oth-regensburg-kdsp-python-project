import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(locator))

    def is_element_present(self, locator):
        elements = self.driver.find_elements(*locator)
        return len(elements) > 0

    def navigate_to(self, url):
        self.driver.get(url)

    def scroll_to_element(self, locator):
        """
        Scrolls the page to the element defined by the locator.

        :param locator: The locator of the element (e.g., (By.XPATH, “//div[@id=‘element’]”)).
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)

    def click_on(self, locator):
        """
        Скроллит до элемента и кликает по нему.

        :param locator: Локатор элемента (например, (By.XPATH, "//button[text()='Submit']")).
        """
        self.scroll_to_element(locator)
        element = self.find_element(locator)
        element.click()

    def try_click(self, locator, retries=3, delay=2):
        """
        Waits for an element to become clickable and clicks on it.
        Implements Retry Pattern for reliability.

        :param locator: The locator of the element (tuple (By, 'locator')).
        :param retries: Number of retries.
        :param delay: The delay between retries (in seconds).
        """
        for attempt in range(1, retries + 1):
            try:
                if attempt > 1:
                    print(f"Attempt {attempt} to wait and click on element with locator {locator}")

                self.scroll_to_element(locator)
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))

                element.click()
                if attempt > 1:
                    print(f"Successfully clicked on element with locator {locator}")
                return

            except Exception as e:
                print(f"Attempt {attempt} failed: {e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    print(f"Failed to click on element with locator {locator} after {retries} attempts")
                    raise