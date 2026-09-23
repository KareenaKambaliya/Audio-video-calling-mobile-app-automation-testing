"""
BasePage provides core element interactions, waits, and utility methods for all page objects.
"""

from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium import webdriver
from appium.webdriver.webelement import WebElement

from config import config
from utils.logger import logger


class BasePage:
    """Base class providing standard mobile interaction methods."""

    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.default_timeout = config.EXPLICIT_WAIT_TIMEOUT

    def find_element(self, locator: tuple[str, str], timeout: int = None) -> WebElement:
        """Wait for element presence and return WebElement."""
        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"Element not found within {timeout}s: {locator}")
            raise

    def find_elements(self, locator: tuple[str, str], timeout: int = None) -> list[WebElement]:
        """Wait for all elements matching locator and return list."""
        timeout = timeout or self.default_timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            return []

    def click(self, locator: tuple[str, str], timeout: int = None):
        """Wait for element to be clickable and click."""
        timeout = timeout or self.default_timeout
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def send_keys(self, locator: tuple[str, str], text: str, timeout: int = None, clear: bool = True):
        """Wait for element, optionally clear, and enter text."""
        element = self.find_element(locator, timeout)
        if clear:
            element.clear()
        element.send_keys(text)

    def is_displayed(self, locator: tuple[str, str], timeout: int = 5) -> bool:
        """Check whether element is visible within timeout without throwing."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_text(self, locator: tuple[str, str], timeout: int = None) -> str:
        """Return visible text from element."""
        return self.find_element(locator, timeout).text

    def take_screenshot(self, prefix: str = "screen") -> str:
        """Capture and save a timestamped screenshot."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        filepath = config.SCREENSHOTS_DIR / filename
        self.driver.save_screenshot(str(filepath))
        logger.info(f"Screenshot captured: {filepath.name}")
        return str(filepath)

    def get_current_package(self) -> str:
        """Return currently active application package name."""
        return self.driver.current_package

    def get_current_activity(self) -> str:
        """Return currently active activity name."""
        return self.driver.current_activity

    def press_back(self):
        """Send back button press."""
        try:
            self.driver.back()
        except Exception as e:
            logger.warning(f"Failed to press back button: {e}")

    def is_text_present(self, text: str, timeout: int = 4) -> bool:
        """Check if any element containing the specified text is visible on screen."""
        from appium.webdriver.common.appiumby import AppiumBy
        locator = (AppiumBy.XPATH, f"//*[contains(@text, '{text}') or contains(@content-desc, '{text}')]")
        return self.is_displayed(locator, timeout=timeout)

    def scroll_to_text(self, text: str):
        """Scrolls vertically to an element containing specific text using UiScrollable or swipes."""
        from appium.webdriver.common.appiumby import AppiumBy
        locator = (AppiumBy.XPATH, f"//*[contains(@text, '{text}') or contains(@content-desc, '{text}')]")
        if self.is_displayed(locator, timeout=2):
            return self.find_element(locator)
        try:
            self.scroll_down()
            if self.is_displayed(locator, timeout=2):
                return self.find_element(locator)
        except Exception:
            pass
        return None

    def scroll_down(self):
        """Perform a quick downward swipe/scroll gesture."""
        try:
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = int(size['height'] * 0.7)
            end_y = int(size['height'] * 0.3)
            self.driver.swipe(start_x, start_y, start_x, end_y, 400)
        except Exception as e:
            logger.warning(f"Scroll gesture failed: {e}")

    def accept_alert_if_present(self, timeout: int = 3) -> bool:
        """Accept an OS dialog/alert if visible."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            self.driver.switch_to.alert.accept()
            return True
        except Exception:
            return False

    def dismiss_alert_if_present(self, timeout: int = 3) -> bool:
        """Dismiss an OS dialog/alert if visible."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            self.driver.switch_to.alert.dismiss()
            return True
        except Exception:
            return False

    def wait_for_activity(self, activity_substring: str, timeout: int = 10) -> bool:
        """Wait until current_activity contains expected substring."""
        import time
        end_time = time.time() + timeout
        while time.time() < end_time:
            current = self.get_current_activity()
            if current and activity_substring.lower() in current.lower():
                return True
            time.sleep(0.5)
        return False
