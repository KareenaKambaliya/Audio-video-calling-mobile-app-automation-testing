"""
Notification Page Object for Plutomen Connect.
Represents NotificationCenterActivity and system push notification handling.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class NotificationPage(BasePage):
    """Page Object for Notification Center and Push Notifications."""

    BTN_NOTIFICATION_BELL = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'notification') or contains(@resource-id, 'iv_notification') or "
        "contains(@resource-id, 'btnNotification') or contains(@content-desc, 'Notification')]"
    )

    NOTIFICATION_ITEM = (
        AppiumBy.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//*[contains(@resource-id, 'tv_title') or "
        "contains(@resource-id, 'txtNotification') or contains(@class, 'RelativeLayout')]"
    )

    EMPTY_NOTIFICATION_VIEW = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'No notifications') or contains(@resource-id, 'PtmNoData') or "
        "contains(@text, 'no notifications')]"
    )

    BTN_CLEAR_ALL = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Clear') or contains(@resource-id, 'btn_clear_all') or "
        "contains(@resource-id, 'tvClearAll')]"
    )

    CONFIRM_CLEAR_DIALOG = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Yes') or contains(@text, 'Clear') or contains(@resource-id, 'button1')]"
    )

    def open_notification_center(self):
        """Navigate to Notification Center screen."""
        logger.info("Opening Notification Center...")
        self.click(self.BTN_NOTIFICATION_BELL, timeout=5)

    def is_notification_center_displayed(self) -> bool:
        """Verify Notification Center screen is open."""
        return (
            "notificationcenteractivity" in self.get_current_activity().lower()
            or self.is_text_present("Notification", timeout=4)
        )

    def tap_first_notification(self):
        """Tap the top notification to navigate to relevant screen."""
        logger.info("Tapping top notification item...")
        self.click(self.NOTIFICATION_ITEM, timeout=4)

    def clear_all_notifications(self):
        """Clear all notification items."""
        logger.info("Clearing all notifications...")
        if self.is_displayed(self.BTN_CLEAR_ALL, timeout=4):
            self.click(self.BTN_CLEAR_ALL)
            if self.is_displayed(self.CONFIRM_CLEAR_DIALOG, timeout=3):
                self.click(self.CONFIRM_CLEAR_DIALOG)

    def is_empty_state_shown(self) -> bool:
        """Verify empty notification placeholder is visible."""
        return self.is_displayed(self.EMPTY_NOTIFICATION_VIEW, timeout=4)

    def open_system_notification_shade(self):
        """Pull down device notification shade."""
        logger.info("Opening Android system notification shade...")
        self.driver.open_notifications()
