"""
Guest Login Page Object for Plutomen Connect.
Represents com.plutomen.ARMS.activity.GuestloginActivity,
GuestLoginNewFlowActivity, and JoinCodeActivity.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class GuestLoginPage(BasePage):
    """Page Object for Guest Login and Join Code flows."""

    GUEST_NAME_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'name') or "
        "contains(@resource-id, 'edtName') or contains(@resource-id, 'etName') or "
        "contains(@hint, 'Name') or contains(@text, 'Name') or "
        "contains(@hint, 'Guest')]"
    )

    JOIN_CODE_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'code') or "
        "contains(@resource-id, 'edtJoinCode') or contains(@resource-id, 'edtCode') or "
        "contains(@hint, 'Code') or contains(@hint, 'code') or "
        "contains(@hint, 'Session ID') or contains(@text, 'Code')]"
    )

    JOIN_BUTTON = (
        AppiumBy.XPATH,
        "//*[(@clickable='true' or contains(@class, 'Button') or contains(@class, 'TextView')) and "
        "(contains(@text, 'Join') or contains(@text, 'JOIN') or "
        "contains(@resource-id, 'btnJoin') or contains(@resource-id, 'btn_join'))]"
    )

    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'error') or contains(@resource-id, 'snackbar') or "
        "contains(@resource-id, 'tv_msg') or contains(@resource-id, 'alert') or "
        "contains(@class, 'Toast')]"
    )

    IN_CALL_OR_WAITING_ROOM = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'WAITING TO JOIN') or contains(@text, 'Waiting') or "
        "contains(@resource-id, 'call') or contains(@resource-id, 'btn_end') or "
        "contains(@text, 'Leave')]"
    )

    def is_guest_login_screen_displayed(self) -> bool:
        """Check if guest login screen is visible."""
        return self.is_displayed(self.JOIN_CODE_INPUT, timeout=5) or "guest" in self.get_current_activity().lower()

    def enter_guest_name(self, name: str):
        """Enter guest user name."""
        logger.info(f"Entering guest name: {name}")
        self.send_keys(self.GUEST_NAME_INPUT, name, timeout=5)

    def enter_join_code(self, code: str):
        """Enter session join code."""
        logger.info(f"Entering join code: {code}")
        self.send_keys(self.JOIN_CODE_INPUT, code, timeout=5)

    def click_join(self):
        """Click the Join session button."""
        logger.info("Clicking Join button...")
        self.click(self.JOIN_BUTTON, timeout=5)

    def login_as_guest(self, name: str, join_code: str):
        """Execute complete guest login flow."""
        if name:
            self.enter_guest_name(name)
        if join_code:
            self.enter_join_code(join_code)
        self.click_join()

    def get_error_message(self) -> str:
        """Extract visible error message."""
        try:
            if self.is_displayed(self.ERROR_MESSAGE, timeout=3):
                return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            pass
        return ""

    def is_joined_successfully(self) -> bool:
        """Check if joined into session or waiting room."""
        return (
            self.is_displayed(self.IN_CALL_OR_WAITING_ROOM, timeout=8)
            or "call" in self.get_current_activity().lower()
            or "webjoin" in self.get_current_activity().lower()
        )
