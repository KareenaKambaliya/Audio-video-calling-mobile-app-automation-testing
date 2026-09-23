"""
Screen Share & Annotation Page Object for Plutomen Connect.
Represents ScheduleShareScreenActivity and ScheduleShareNonARScreenActivity.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class ScreenSharePage(BasePage):
    """Page Object for AR & Non-AR Screen Sharing and AR Annotations."""

    BTN_SHARE_SCREEN = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'share') or contains(@resource-id, 'ivShare') or "
        "contains(@resource-id, 'btn_share') or contains(@content-desc, 'Share Screen')]"
    )

    OPTION_AR_MODE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'AR') or contains(@resource-id, 'btn_ar_share')]"
    )

    OPTION_NON_AR_MODE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Non-AR') or contains(@resource-id, 'btn_non_ar_share')]"
    )

    BTN_STOP_SHARE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Stop Share') or contains(@text, 'STOP') or "
        "contains(@resource-id, 'btn_stop_share') or contains(@content-desc, 'Stop Share')]"
    )

    # Annotation Toolbar Locators
    TOOLBAR_ANNOTATION = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'activity_annotationlist') or contains(@resource-id, 'toolbar') or "
        "contains(@resource-id, 'colorrecyclerview')]"
    )

    BTN_FREEZE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Freeze') or contains(@resource-id, 'btn_freeze') or contains(@content-desc, 'Freeze')]"
    )

    BTN_PEN = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'pen') or contains(@resource-id, 'draw') or contains(@content-desc, 'Pen')]"
    )

    def start_screen_share(self, mode: str = "AR"):
        """Initiate screen sharing in AR or Non-AR mode."""
        logger.info(f"Starting screen share in {mode} mode...")
        if self.is_displayed(self.BTN_SHARE_SCREEN, timeout=4):
            self.click(self.BTN_SHARE_SCREEN)

        if "non-ar" in mode.lower():
            if self.is_displayed(self.OPTION_NON_AR_MODE, timeout=3):
                self.click(self.OPTION_NON_AR_MODE)
        else:
            if self.is_displayed(self.OPTION_AR_MODE, timeout=3):
                self.click(self.OPTION_AR_MODE)

        # Handle OS media projection prompt if presented ("Start now")
        self.accept_system_media_projection()

    def accept_system_media_projection(self):
        """Click 'Start now' on Android Screen Capture Assistant dialog if shown."""
        btn_start_now = (
            AppiumBy.XPATH,
            "//*[contains(@text, 'Start now') or contains(@text, 'START NOW') or contains(@resource-id, 'android:id/button1')]"
        )
        if self.is_displayed(btn_start_now, timeout=3):
            logger.info("Accepting OS screen recording / casting permission...")
            self.click(btn_start_now)

    def is_screen_share_active(self) -> bool:
        """Verify screen share is running."""
        return (
            self.is_displayed(self.BTN_STOP_SHARE, timeout=5)
            or "sharescreen" in self.get_current_activity().lower()
        )

    def are_annotations_available(self) -> bool:
        """Check if AR annotation tools (pen, freeze, palette) are active."""
        return (
            self.is_displayed(self.TOOLBAR_ANNOTATION, timeout=4)
            or self.is_displayed(self.BTN_PEN, timeout=4)
            or self.is_displayed(self.BTN_FREEZE, timeout=4)
        )

    def stop_screen_share(self):
        """Stop screen share."""
        logger.info("Stopping screen share...")
        if self.is_displayed(self.BTN_STOP_SHARE, timeout=4):
            self.click(self.BTN_STOP_SHARE)
