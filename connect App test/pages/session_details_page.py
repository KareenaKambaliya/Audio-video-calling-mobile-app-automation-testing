"""
Session Details Page Object for Plutomen Connect.
Represents com.plutomen.ARMS.activity.SessionDetailsActivity.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class SessionDetailsPage(BasePage):
    """Page Object for Post-Call Summary, Session Details, and Recordings."""

    SESSION_TITLE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_session_title') or contains(@resource-id, 'tvSessionId') or "
        "contains(@text, 'Session Detail')]"
    )

    SESSION_DURATION = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_duration') or contains(@resource-id, 'llSessionTimeLine')]"
    )

    SESSION_PARTICIPANTS = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_participants') or contains(@resource-id, 'rc_participants')]"
    )

    MEDIA_RECORDING_VIEW = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'exo_styled_player_view') or contains(@resource-id, 'ivUserRecording') or "
        "contains(@resource-id, 'exo_player_view') or contains(@text, 'Recording')]"
    )

    BTN_SHARE_SESSION = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'session_share') or contains(@resource-id, 'imgSessionShare') or "
        "contains(@content-desc, 'Share') or contains(@text, 'Share')]"
    )

    HISTORICAL_SESSION_ROW = (
        AppiumBy.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//*[contains(@resource-id, 'relSession') or "
        "contains(@resource-id, 'tvActiveSession') or contains(@class, 'RelativeLayout')]"
    )

    def is_session_details_displayed(self) -> bool:
        """Verify Session Details screen is open."""
        return (
            "sessiondetailsactivity" in self.get_current_activity().lower()
            or self.is_displayed(self.SESSION_TITLE, timeout=5)
        )

    def open_historical_session(self):
        """Open a past session from session list."""
        logger.info("Opening past session details from list...")
        self.click(self.HISTORICAL_SESSION_ROW, timeout=5)

    def has_recording(self) -> bool:
        """Check whether session has a playable recording attachment."""
        return self.is_displayed(self.MEDIA_RECORDING_VIEW, timeout=4)

    def share_session_report(self):
        """Click share session report."""
        logger.info("Sharing session report...")
        self.click(self.BTN_SHARE_SESSION, timeout=4)
