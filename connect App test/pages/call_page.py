"""
Call Page Object for Plutomen Connect.
Handles CallActivity, CallRecieveActivity, and CallInfoActivity.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class CallPage(BasePage):
    """Page Object for initiating, receiving, managing, and viewing info for 1-on-1 calls."""

    # --- Call Initiation Locators ---
    BTN_CREATE_CALL = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Create') or contains(@resource-id, 'btn_create') or "
        "contains(@resource-id, 'btnCreateCall') or contains(@resource-id, 'fab_call')]"
    )

    SEARCH_CONTACT_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'search') or contains(@hint, 'Search') or "
        "contains(@hint, 'Enter email') or contains(@hint, 'contact')]"
    )

    CONTACT_ITEM = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'txtUserName') or contains(@resource-id, 'tv_name') or "
        "contains(@resource-id, 'layout_contact') or contains(@class, 'RelativeLayout')]"
    )

    BTN_VIDEO_CALL = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'iv_video_call') or contains(@resource-id, 'btnVideo') or "
        "contains(@resource-id, 'ic_call_answer_video') or contains(@content-desc, 'Video Call') or "
        "contains(@text, 'Video')]"
    )

    BTN_AUDIO_CALL = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'iv_audio_call') or contains(@resource-id, 'btnAudio') or "
        "contains(@resource-id, 'ic_call') or contains(@content-desc, 'Audio Call') or "
        "contains(@text, 'Audio')]"
    )

    # --- Active In-Call Controls ---
    BTN_END_CALL = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'call_end') or contains(@resource-id, 'btn_end') or "
        "contains(@resource-id, 'callend') or contains(@content-desc, 'End Call') or "
        "contains(@resource-id, 'ivEndCall')]"
    )

    BTN_MUTE_AUDIO = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'mute') or contains(@resource-id, 'ic_audio_off') or "
        "contains(@resource-id, 'ivMute') or contains(@content-desc, 'Mute')]"
    )

    BTN_TOGGLE_VIDEO = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'camera') or contains(@resource-id, 'video_on_off') or "
        "contains(@resource-id, 'ivCamera') or contains(@content-desc, 'Camera')]"
    )

    CALL_TIMER = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_duration') or contains(@resource-id, 'timer') or "
        "contains(@resource-id, 'tvCallDuration') or contains(@text, ':')]"
    )

    # --- Incoming Call Locators (CallRecieveActivity) ---
    CALLER_NAME = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_caller_name') or contains(@resource-id, 'txtCaller') or "
        "contains(@resource-id, 'tv_name')]"
    )

    BTN_ACCEPT_CALL = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'accept') or contains(@resource-id, 'ic_call_answer') or "
        "contains(@resource-id, 'btnAccept') or contains(@content-desc, 'Accept')]"
    )

    BTN_REJECT_CALL = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'decline') or contains(@resource-id, 'ic_call_decline') or "
        "contains(@resource-id, 'btnReject') or contains(@content-desc, 'Decline')]"
    )

    # --- Call Info Locators (CallInfoActivity) ---
    BTN_CALL_INFO = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'info') or contains(@resource-id, 'ic_info') or "
        "contains(@resource-id, 'btnInfo') or contains(@content-desc, 'Call Info')]"
    )

    CALL_INFO_PARTICIPANT = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_participant') or contains(@resource-id, 'txtParticipant')]"
    )

    CALL_INFO_DURATION = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_duration') or contains(@resource-id, 'exo_duration')]"
    )

    # --- Error / Notification Banner ---
    CALL_ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'offline') or contains(@text, 'not found') or "
        "contains(@text, 'Failed') or contains(@text, 'Rejected') or "
        "contains(@text, 'Network error') or contains(@resource-id, 'error')]"
    )

    def start_call(self, recipient: str, call_type: str = "Video"):
        """Initiate video or audio call to recipient."""
        logger.info(f"Initiating {call_type} call to '{recipient}'...")
        if self.is_displayed(self.BTN_CREATE_CALL, timeout=4):
            self.click(self.BTN_CREATE_CALL)

        if recipient and self.is_displayed(self.SEARCH_CONTACT_INPUT, timeout=4):
            self.send_keys(self.SEARCH_CONTACT_INPUT, recipient)
            time.sleep(1)
            if self.is_displayed(self.CONTACT_ITEM, timeout=3):
                self.click(self.CONTACT_ITEM)

        if call_type.lower() == "audio":
            if self.is_displayed(self.BTN_AUDIO_CALL, timeout=3):
                self.click(self.BTN_AUDIO_CALL)
        else:
            if self.is_displayed(self.BTN_VIDEO_CALL, timeout=3):
                self.click(self.BTN_VIDEO_CALL)

    def is_call_active(self) -> bool:
        """Check if call is currently connected and active."""
        return (
            self.is_displayed(self.BTN_END_CALL, timeout=6)
            or "callactivity" in self.get_current_activity().lower()
        )

    def end_call(self):
        """End the ongoing active call."""
        logger.info("Ending call...")
        if self.is_displayed(self.BTN_END_CALL, timeout=4):
            self.click(self.BTN_END_CALL)
            time.sleep(2)

    def is_incoming_call_displayed(self) -> bool:
        """Check if incoming call screen (CallRecieveActivity) is active."""
        return (
            self.is_displayed(self.BTN_ACCEPT_CALL, timeout=4)
            or "callrecieveactivity" in self.get_current_activity().lower()
        )

    def accept_incoming_call(self):
        """Accept an incoming call."""
        logger.info("Accepting incoming call...")
        self.click(self.BTN_ACCEPT_CALL, timeout=4)

    def reject_incoming_call(self):
        """Reject an incoming call."""
        logger.info("Rejecting incoming call...")
        self.click(self.BTN_REJECT_CALL, timeout=4)

    def open_call_info(self):
        """Open Call Info screen / dialog."""
        logger.info("Opening Call Info...")
        self.click(self.BTN_CALL_INFO, timeout=4)

    def is_call_info_displayed(self) -> bool:
        """Verify call info details are visible."""
        return (
            self.is_displayed(self.CALL_INFO_DURATION, timeout=4)
            or "callinfoactivity" in self.get_current_activity().lower()
        )

    def get_error_message(self) -> str:
        """Extract call failure error message."""
        try:
            if self.is_displayed(self.CALL_ERROR_MESSAGE, timeout=3):
                return self.get_text(self.CALL_ERROR_MESSAGE)
        except Exception:
            pass
        return ""
