"""
Schedule Page Object for Plutomen Connect.
Handles CreateScheduleActivity, ScheduleCallDetailsActivity, and ScheduleCallJoiningActivity.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class SchedulePage(BasePage):
    """Page Object for Creating, Joining, Viewing Details and Managing Scheduled Sessions."""

    # --- Home / Entry Locators ---
    BTN_NAV_SCHEDULE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Schedule') or contains(@resource-id, 'btn_schedule') or "
        "contains(@resource-id, 'layout_schedule')]"
    )

    # --- Create Schedule Locators ---
    TITLE_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'title') or contains(@hint, 'Title') or "
        "contains(@hint, 'Enter Schedule Title') or contains(@resource-id, 'edtTitle')]"
    )

    PARTICIPANT_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'participant') or contains(@hint, 'participant') or "
        "contains(@hint, 'email') or contains(@resource-id, 'edtParticipant')]"
    )

    DATE_TIME_PICKER = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'time') or contains(@resource-id, 'date') or "
        "contains(@resource-id, 'layout_date') or contains(@text, 'Date')]"
    )

    BTN_CONFIRM_PICKER = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'OK') or contains(@text, 'Confirm') or contains(@resource-id, 'button1')]"
    )

    BTN_SUBMIT_SCHEDULE = (
        AppiumBy.XPATH,
        "//*[(@clickable='true' or contains(@class, 'Button') or contains(@class, 'TextView')) and "
        "(contains(@text, 'Create Schedule') or contains(@text, 'Schedule') or "
        "contains(@text, 'Save') or contains(@resource-id, 'btn_save_schedule'))]"
    )

    # --- Schedule Details Locators (ScheduleCallDetailsActivity) ---
    DETAILS_TITLE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_title') or contains(@resource-id, 'txtScheduleTitle')]"
    )

    DETAILS_PARTICIPANTS = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'rv_participants') or contains(@resource-id, 'txtParticipants')]"
    )

    BTN_RESCHEDULE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Reschedule') or contains(@text, 'Edit') or contains(@resource-id, 'btn_reschedule')]"
    )

    BTN_CANCEL_SCHEDULE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Cancel Schedule') or contains(@text, 'Delete') or contains(@resource-id, 'btn_cancel_schedule')]"
    )

    CONFIRM_CANCEL_POPUP = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Yes') or contains(@text, 'Delete') or contains(@resource-id, 'android:id/button1')]"
    )

    # --- Schedule Joining Locators (ScheduleCallJoiningActivity) ---
    BTN_JOIN_SCHEDULED = (
        AppiumBy.XPATH,
        "//*[(@clickable='true' or contains(@class, 'Button') or contains(@class, 'TextView')) and "
        "(contains(@text, 'Join') or contains(@text, 'JOIN') or contains(@resource-id, 'btn_join'))]"
    )

    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'error') or contains(@resource-id, 'snackbar') or "
        "contains(@resource-id, 'tv_msg') or contains(@class, 'Toast') or "
        "contains(@text, 'past') or contains(@text, 'cancelled') or contains(@text, 'not started')]"
    )

    def navigate_to_create_schedule(self):
        """Navigate to Create Schedule screen."""
        logger.info("Opening Create Schedule screen...")
        self.click(self.BTN_NAV_SCHEDULE, timeout=5)

    def is_create_schedule_screen_displayed(self) -> bool:
        """Check if Create Schedule form is active."""
        return self.is_displayed(self.TITLE_INPUT, timeout=5) or "createschedule" in self.get_current_activity().lower()

    def fill_schedule_form(self, title: str, date_time: str, participant: str):
        """Fill scheduled session parameters."""
        logger.info(f"Filling schedule: Title='{title}', Participant='{participant}'")
        if title:
            self.send_keys(self.TITLE_INPUT, title, timeout=5)
        if participant:
            self.send_keys(self.PARTICIPANT_INPUT, participant, timeout=5)

    def submit_schedule(self):
        """Click create schedule button."""
        logger.info("Submitting scheduled session...")
        self.click(self.BTN_SUBMIT_SCHEDULE, timeout=5)

    def is_schedule_created(self) -> bool:
        """Verify session creation success."""
        return (
            "details" in self.get_current_activity().lower()
            or self.is_text_present("Schedule created", timeout=4)
            or not self.is_displayed(self.TITLE_INPUT, timeout=3)
        )

    def join_scheduled_call(self):
        """Attempt to join scheduled call."""
        logger.info("Clicking Join on scheduled session...")
        self.click(self.BTN_JOIN_SCHEDULED, timeout=5)

    def cancel_schedule(self):
        """Cancel/Delete the scheduled session."""
        logger.info("Cancelling scheduled session...")
        if self.is_displayed(self.BTN_CANCEL_SCHEDULE, timeout=4):
            self.click(self.BTN_CANCEL_SCHEDULE)
            if self.is_displayed(self.CONFIRM_CANCEL_POPUP, timeout=3):
                self.click(self.CONFIRM_CANCEL_POPUP)

    def get_error_message(self) -> str:
        """Extract visible error or rejection message."""
        try:
            if self.is_displayed(self.ERROR_MESSAGE, timeout=3):
                return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            pass
        return ""
