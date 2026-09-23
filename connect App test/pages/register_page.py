"""
Register Page Object for Plutomen Connect.
Represents com.plutomen.ARMS.activity.RegisterActivity.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class RegisterPage(BasePage):
    """Page Object for User Registration Screen."""

    NAME_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'name') or "
        "contains(@resource-id, 'edtName') or contains(@resource-id, 'etName') or "
        "contains(@hint, 'Name') or contains(@text, 'Name')]"
    )

    EMAIL_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'email') or "
        "contains(@resource-id, 'edtEmail') or contains(@resource-id, 'etEmail') or "
        "contains(@hint, 'Email') or contains(@text, 'Email')]"
    )

    PASSWORD_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[(@password='true' or contains(@resource-id, 'edtPassword') "
        "or contains(@resource-id, 'etPassword')) and not(contains(@resource-id, 'Confirm') "
        "or contains(@resource-id, 'confirm'))]"
    )

    CONFIRM_PASSWORD_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'Confirm') or "
        "contains(@resource-id, 'confirm') or contains(@hint, 'Confirm') or "
        "contains(@text, 'Confirm')]"
    )

    REGISTER_BUTTON = (
        AppiumBy.XPATH,
        "//*[(@clickable='true' or contains(@class, 'Button') or contains(@class, 'TextView')) and "
        "(contains(@text, 'Register') or contains(@text, 'REGISTER') or "
        "contains(@text, 'Sign Up') or contains(@text, 'SIGN UP') or "
        "contains(@resource-id, 'btnRegister') or contains(@resource-id, 'btn_register'))]"
    )

    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'error') or contains(@resource-id, 'snackbar') or "
        "contains(@resource-id, 'tv_msg') or contains(@resource-id, 'alert') or "
        "contains(@class, 'Toast')]"
    )

    SUCCESS_INDICATOR = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Success') or contains(@text, 'Verification') or "
        "contains(@text, 'Login') or contains(@resource-id, 'success')]"
    )

    def is_register_screen_displayed(self) -> bool:
        """Check if registration screen is displayed."""
        return self.is_displayed(self.NAME_INPUT, timeout=5) or "register" in self.get_current_activity().lower()

    def fill_registration_form(self, name: str, email: str, password: str, confirm_password: str):
        """Fill all fields in registration form."""
        logger.info(f"Filling registration: Name='{name}', Email='{email}'")
        if name:
            self.send_keys(self.NAME_INPUT, name, timeout=5)
        if email:
            self.send_keys(self.EMAIL_INPUT, email, timeout=5)
        if password:
            self.send_keys(self.PASSWORD_INPUT, password, timeout=5)
        if confirm_password:
            self.send_keys(self.CONFIRM_PASSWORD_INPUT, confirm_password, timeout=5)

    def click_register(self):
        """Click register/submit button."""
        logger.info("Submitting registration form...")
        self.click(self.REGISTER_BUTTON, timeout=5)

    def get_error_message(self) -> str:
        """Extract visible error message."""
        try:
            if self.is_displayed(self.ERROR_MESSAGE, timeout=3):
                return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            pass
        return ""

    def is_registration_successful(self) -> bool:
        """Verify registration success."""
        return self.is_displayed(self.SUCCESS_INDICATOR, timeout=5) or "login" in self.get_current_activity().lower()
