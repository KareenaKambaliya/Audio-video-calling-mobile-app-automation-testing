"""
Share Into App Page Object for Plutomen Connect.
Represents com.plutomen.ARMS.activity.SharingActivity.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class SharingPage(BasePage):
    """Page Object for incoming shared content (text, image, documents)."""

    SHARING_CONTAINER = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'SharingActivity') or contains(@resource-id, 'layoutShare') or "
        "contains(@text, 'Send to') or contains(@text, 'Share')]"
    )

    CHAT_TARGET_ITEM = (
        AppiumBy.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//*[contains(@resource-id, 'tv_name') or "
        "contains(@resource-id, 'txtUserName') or contains(@class, 'RelativeLayout')]"
    )

    BTN_SEND_SHARE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Send') or contains(@resource-id, 'btn_send')]"
    )

    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'not supported') or contains(@resource-id, 'error') or contains(@resource-id, 'snackbar')]"
    )

    def is_share_screen_displayed(self) -> bool:
        """Verify app handled incoming share intent."""
        return (
            "sharingactivity" in self.get_current_activity().lower()
            or self.is_displayed(self.SHARING_CONTAINER, timeout=5)
        )

    def select_chat_recipient(self):
        """Select contact to share content with."""
        logger.info("Selecting chat recipient for shared content...")
        self.click(self.CHAT_TARGET_ITEM, timeout=4)

    def click_send_shared_content(self):
        """Send shared content into chosen chat."""
        logger.info("Sending shared content...")
        self.click(self.BTN_SEND_SHARE, timeout=4)

    def get_error_message(self) -> str:
        """Extract unsupported file format error message."""
        try:
            if self.is_displayed(self.ERROR_MESSAGE, timeout=3):
                return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            pass
        return ""
