"""
Home Page Object for Plutomen Connect Application.
Represents dashboard and main navigation elements.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class HomePage(BasePage):
    """Page Object for Plutomen Connect main dashboard screen."""

    # --- Locators ---
    TITLE_LETS_BEGIN = (AppiumBy.XPATH, "//*[contains(@text, \"Let's begin!\")]")
    BTN_CREATE = (AppiumBy.XPATH, "//*[contains(@text, 'Create')]")
    BTN_JOIN = (AppiumBy.XPATH, "//*[contains(@text, 'Join')]")
    BTN_SCHEDULE = (AppiumBy.XPATH, "//*[contains(@text, 'Schedule')]")
    BTN_SELF_MODE = (AppiumBy.XPATH, "//*[contains(@text, 'Self Mode')]")

    # --- Actions ---
    def is_app_in_foreground(self) -> bool:
        """Check if Plutomen Connect package is currently running in foreground."""
        current_pkg = self.get_current_package()
        return "plutomen" in str(current_pkg).lower()

    def is_dashboard_visible(self) -> bool:
        """Check if main dashboard elements are visible."""
        return self.is_displayed(self.TITLE_LETS_BEGIN, timeout=5)
