"""
Web Join and Deep Link Page Object for Plutomen Connect.
Represents com.plutomen.ARMS.activity.webjoinActivity.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class WebJoinPage(BasePage):
    """Page Object for Web Join & Deep Link handling."""

    READY_TO_JOIN_HEADER = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Ready to join?') or contains(@text, 'Join') or "
        "contains(@resource-id, 'tv_title')]"
    )

    JOIN_NOW_BUTTON = (
        AppiumBy.XPATH,
        "//*[(@clickable='true' or contains(@class, 'Button') or contains(@class, 'TextView')) and "
        "(contains(@text, 'Join now') or contains(@text, 'Join Session') or contains(@text, 'JOIN') or "
        "contains(@resource-id, 'btnJoin'))]"
    )

    SESSION_STATUS_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'no longer available') or contains(@text, 'expired') or "
        "contains(@text, 'ended') or contains(@resource-id, 'tv_status') or "
        "contains(@resource-id, 'error') or contains(@resource-id, 'snackbar')]"
    )

    def is_join_screen_displayed(self) -> bool:
        """Verify webjoin screen is active."""
        return (
            self.is_displayed(self.JOIN_NOW_BUTTON, timeout=6)
            or self.is_displayed(self.READY_TO_JOIN_HEADER, timeout=6)
            or "webjoin" in self.get_current_activity().lower()
        )

    def click_join_now(self):
        """Click join session button."""
        logger.info("Clicking Join Now...")
        self.click(self.JOIN_NOW_BUTTON, timeout=5)

    def get_status_or_error_message(self) -> str:
        """Extract status or error message (e.g. expired session)."""
        try:
            if self.is_displayed(self.SESSION_STATUS_MESSAGE, timeout=4):
                return self.get_text(self.SESSION_STATUS_MESSAGE)
        except Exception:
            pass
        return ""
