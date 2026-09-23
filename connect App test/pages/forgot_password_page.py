"""
Forgot Password Page Object for Plutomen Connect.
Represents com.plutomen.ARMS.activity.ForgotpasswordActivity.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class ForgotPasswordPage(BasePage):
    """Page Object for Forgot Password Screen."""

    EMAIL_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'email') or "
        "contains(@resource-id, 'edtEmail') or contains(@resource-id, 'etEmail') or "
        "contains(@hint, 'Email') or contains(@text, 'Email')]"
    )

    SUBMIT_BUTTON = (
        AppiumBy.XPATH,
        "//*[(@clickable='true' or contains(@class, 'Button') or contains(@class, 'TextView')) and "
        "(contains(@text, 'Submit') or contains(@text, 'Send') or contains(@text, 'Reset') or "
        "contains(@resource-id, 'btnSubmit') or contains(@resource-id, 'btnSend') or "
        "contains(@resource-id, 'btn_forgot'))]"
    )

    SUCCESS_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'sent') or contains(@text, 'Check your email') or "
        "contains(@text, 'Reset password link') or contains(@resource-id, 'tvSuccess')]"
    )

    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'error') or contains(@resource-id, 'snackbar') or "
        "contains(@resource-id, 'tv_msg') or contains(@class, 'Toast') or "
        "contains(@resource-id, 'alert')]"
    )

    def is_forgot_password_screen_displayed(self) -> bool:
        """Check if forgot password screen is displayed."""
        return self.is_displayed(self.EMAIL_INPUT, timeout=5) or "forgot" in self.get_current_activity().lower()

    def enter_email(self, email: str):
        """Enter email address for password reset."""
        logger.info(f"Entering reset email: {email}")
        self.send_keys(self.EMAIL_INPUT, email, timeout=5)

    def click_submit(self):
        """Click submit/reset button."""
        logger.info("Clicking Submit on Forgot Password screen...")
        self.click(self.SUBMIT_BUTTON, timeout=5)

    def request_password_reset(self, email: str):
        """Complete forgot password request."""
        if email:
            self.enter_email(email)
        self.click_submit()

    def get_error_message(self) -> str:
        """Extract visible error message."""
        try:
            if self.is_displayed(self.ERROR_MESSAGE, timeout=3):
                return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            pass
        return ""

    def is_reset_email_sent(self) -> bool:
        """Verify success confirmation message."""
        return self.is_displayed(self.SUCCESS_MESSAGE, timeout=5)
