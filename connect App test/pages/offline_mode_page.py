"""
Offline Self-Mode Page Object for Plutomen Connect.
Represents OfflineSelfmodeDetailsActivity and ScheduleShareScreenOfflineActivity.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class OfflineModePage(BasePage):
    """Page Object for Self Mode and Offline Guided Sessions."""

    BTN_SELF_MODE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Self Mode') or contains(@resource-id, 'tvSelfMode') or "
        "contains(@resource-id, 'llSelfOffline') or contains(@content-desc, 'Self Mode')]"
    )

    SELF_MODE_TITLE_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'edt_title') or contains(@hint, 'Title') or "
        "contains(@hint, 'Self Mode Title') or contains(@resource-id, 'edtSelfModeTitle')]"
    )

    BTN_START_SESSION = (
        AppiumBy.XPATH,
        "//*[(@clickable='true' or contains(@class, 'Button') or contains(@class, 'TextView')) and "
        "(contains(@text, 'Start') or contains(@text, 'START') or "
        "contains(@resource-id, 'btnStartSession') or contains(@resource-id, 'btn_start'))]"
    )

    OPTION_AR_MODE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'AR') or contains(@resource-id, 'btnAR')]"
    )

    OPTION_NON_AR_MODE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Non-AR') or contains(@resource-id, 'btnNonAR')]"
    )

    OFFLINE_SESSION_VIEW = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'activity_offline_selfmode_details') or "
        "contains(@resource-id, 'rcSelfModeCallList') or contains(@text, 'Self Mode')]"
    )

    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'error') or contains(@resource-id, 'tv_msg') or "
        "contains(@text, 'unavailable') or contains(@text, 'Enter Self Mode Title')]"
    )

    def navigate_to_self_mode(self):
        """Navigate to Self Mode screen."""
        logger.info("Opening Self Mode...")
        self.click(self.BTN_SELF_MODE, timeout=5)

    def start_self_mode_session(self, title: str = "Test Self Mode", mode: str = "AR"):
        """Initiate self-mode offline session."""
        logger.info(f"Starting Self Mode session: Title='{title}', Mode='{mode}'...")
        if self.is_displayed(self.SELF_MODE_TITLE_INPUT, timeout=4):
            self.send_keys(self.SELF_MODE_TITLE_INPUT, title)

        if "non-ar" in mode.lower():
            if self.is_displayed(self.OPTION_NON_AR_MODE, timeout=3):
                self.click(self.OPTION_NON_AR_MODE)
        else:
            if self.is_displayed(self.OPTION_AR_MODE, timeout=3):
                self.click(self.OPTION_AR_MODE)

        if self.is_displayed(self.BTN_START_SESSION, timeout=4):
            self.click(self.BTN_START_SESSION)

    def is_session_active(self) -> bool:
        """Verify offline self-mode session is started."""
        return (
            self.is_displayed(self.OFFLINE_SESSION_VIEW, timeout=5)
            or "selfmode" in self.get_current_activity().lower()
            or "offline" in self.get_current_activity().lower()
        )

    def get_error_message(self) -> str:
        """Extract visible error message."""
        try:
            if self.is_displayed(self.ERROR_MESSAGE, timeout=3):
                return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            pass
        return ""
