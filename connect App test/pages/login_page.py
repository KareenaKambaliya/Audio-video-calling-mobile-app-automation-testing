"""
Login Page Object for Plutomen Connect Application.
Handles username/email, password inputs, dialog dismissal, navigation to register/forgot password/guest login, and logout.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class LoginPage(BasePage):
    """Page Object representing the Plutomen Connect Login screen."""

    # --- Input Locators ---
    EMAIL_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'email') or "
        "contains(@resource-id, 'username') or "
        "contains(@resource-id, 'edt_email') or "
        "contains(@resource-id, 'etEmail') or "
        "contains(@resource-id, 'edtEmail') or "
        "contains(@hint, 'Email') or contains(@hint, 'email') or "
        "contains(@text, 'Email') or contains(@text, 'email')]"
    )

    PASSWORD_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'edt_pwd') or "
        "@password='true' or "
        "contains(@resource-id, 'password') or "
        "contains(@resource-id, 'edtPassword') or "
        "contains(@resource-id, 'etPassword') or "
        "contains(@hint, 'Password') or contains(@hint, 'password')]"
    )

    LOGIN_BUTTON = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'btn_reg') or "
        "((@text='Login' or @text='LOGIN') and (@clickable='true' or contains(@class, 'Button') or contains(@class, 'TextView')))]"
    )

    # --- Auth Navigation Links ---
    REGISTER_LINK = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Register') or contains(@text, 'Sign Up') or "
        "contains(@resource-id, 'register') or contains(@resource-id, 'txtRegister') or "
        "contains(@resource-id, 'btn_register')]"
    )

    FORGOT_PASSWORD_LINK = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'txt_forgotpwd') or contains(@text, 'Forgot Password') or contains(@text, 'Forgot')]"
    )

    GUEST_LOGIN_LINK = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'txt_guestlogin') or contains(@text, 'Join with Code') or "
        "contains(@text, 'Guest') or contains(@resource-id, 'btn_guest')]"
    )

    # --- Dashboard / Navigation Locators ---
    DASHBOARD_INDICATOR = (
        AppiumBy.XPATH,
        "//*[contains(@text, \"Let's begin!\") or contains(@text, 'Create') or contains(@text, 'Self Mode')]"
    )

    SETTINGS_TAB = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'llsettings') or contains(@resource-id, 'img_settings')]"
    )

    PROFILE_ICON = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Profile') or contains(@resource-id, 'profile') or "
        "contains(@resource-id, 'llsettings') or contains(@resource-id, 'img_settings')]"
    )

    PROFILE_ITEM = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Profile') or contains(@resource-id, 'txt_profile') or contains(@resource-id, 'profile')]"
    )

    LOGOUT_BUTTON = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'btn_logout') or contains(@text, 'Logout') or "
        "contains(@text, 'Log out') or contains(@text, 'LOGOUT')]"
    )

    CONFIRM_LOGOUT_BUTTON = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'YES') or contains(@text, 'Yes') or contains(@text, 'Confirm') or contains(@text, 'OK')]"
    )

    # --- Dialog / Popup Locators ---
    UPDATE_POPUP = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'New version is available') or contains(@text, 'UPDATE')]"
    )

    SECURITY_PROMPT = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'USB Debugging') or contains(@text, 'Developer Options')]"
    )

    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'error') or contains(@resource-id, 'snackbar') or "
        "contains(@resource-id, 'alert') or contains(@resource-id, 'tv_msg') or "
        "contains(@resource-id, 'tvError') or contains(@class, 'Toast')]"
    )

    # --- Modal Alert Dialog Locators (e.g. "Server error", "Invalid credentials") ---
    ALERT_DIALOG = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'alertTitle') or contains(@resource-id, 'parentPanel') or "
        "contains(@text, 'Plutomen Connect') or contains(@resource-id, 'message')]"
    )
    ALERT_TITLE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'alertTitle') or contains(@text, 'Plutomen Connect')]"
    )
    ALERT_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'message') or contains(@resource-id, 'tv_msg') or contains(@resource-id, 'txt_msg')]"
    )
    ALERT_OK_BUTTON = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'button1') or @text='OK' or @text='Ok' or @text='ok' or "
        "contains(@text, 'OK') or contains(@resource-id, 'btn_ok') or contains(@resource-id, 'btnOk')]"
    )

    def dismiss_popup_dialog(self, timeout: int = 2) -> str:
        """
        Check if an error or alert modal dialog (such as 'Server error' with an 'OK' button)
        is blocking the screen. Reads the message, clicks 'OK' to dismiss it, and returns the message text.
        """
        message = ""
        try:
            # 1. Read message text if visible
            if self.is_displayed(self.ALERT_MESSAGE, timeout=timeout):
                try:
                    message = self.get_text(self.ALERT_MESSAGE)
                except Exception:
                    pass

            # 2. Click OK button to dismiss dialog
            if self.is_displayed(self.ALERT_OK_BUTTON, timeout=timeout):
                logger.info(f"Modal popup dialog detected ('{message}'). Clicking OK to dismiss...")
                try:
                    self.click(self.ALERT_OK_BUTTON, timeout=3)
                    time.sleep(1)
                except Exception:
                    # Coordinate tap fallback for OK button
                    try:
                        btn = self.find_element(self.ALERT_OK_BUTTON, timeout=2)
                        btn.click()
                    except Exception:
                        self.driver.back()
                return message
        except Exception as e:
            logger.debug(f"Popup check: {e}")

        # Fallback to standard alert dismissal
        try:
            if self.accept_alert_if_present(timeout=1):
                logger.info("Accepted OS alert dialog.")
        except Exception:
            pass

        return message

    def dismiss_initial_dialogs(self):
        """
        Detect and dismiss blocking popups (e.g. Update available, Developer mode notice,
        or leftover Server error / alert dialogs).
        """
        logger.info("Checking for initial popups or blocking dialogs...")
        # Always dismiss any modal dialog first (e.g. from previous run)
        self.dismiss_popup_dialog(timeout=1)

        for _ in range(2):
            has_update = self.is_displayed(self.UPDATE_POPUP, timeout=1)
            has_security = self.is_displayed(self.SECURITY_PROMPT, timeout=1)

            if has_update or has_security:
                prompt_type = "Update" if has_update else "Security/DevOptions"
                logger.info(f"Detected {prompt_type} dialog. Sending Android BACK key to dismiss...")
                try:
                    self.driver.back()
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Could not press BACK: {e}")
            else:
                break

    def is_login_screen_displayed(self) -> bool:
        """Check if login input fields are visible."""
        return self.is_displayed(self.EMAIL_INPUT, timeout=4)

    def is_already_logged_in(self) -> bool:
        """Check if user is already logged in (Dashboard is active)."""
        return self.is_displayed(self.DASHBOARD_INDICATOR, timeout=3)

    def is_logged_in(self) -> bool:
        """Alias for is_already_logged_in."""
        return self.is_already_logged_in()

    def enter_email(self, email: str):
        """Enter user email or username (safely clearing previous text first)."""
        logger.info(f"Entering email: '{email}'")
        elem = self.find_element(self.EMAIL_INPUT, timeout=6)
        elem.clear()
        if email:
            elem.send_keys(email)

    def enter_password(self, password: str):
        """Enter user password (safely clearing previous text first)."""
        logger.info("Entering password...")
        elem = self.find_element(self.PASSWORD_INPUT, timeout=6)
        elem.clear()
        if password:
            elem.send_keys(password)

    def click_login(self):
        """Click the Login/Sign-In button with robust multi-strategy fallback."""
        logger.info("Clicking Login button...")
        try:
            self.hide_keyboard()
            time.sleep(0.5)
        except Exception:
            pass

        # Strategy 1: Standard Appium click on verified LOGIN_BUTTON locator
        try:
            btn = self.find_element(self.LOGIN_BUTTON, timeout=8)
            btn.click()
            logger.info("Successfully clicked Login button via element.click()")
            return
        except Exception as e:
            logger.warning(f"Standard click on Login button failed: {e}. Trying tap by coordinates...")

        # Strategy 2: Tap on element coordinates
        try:
            btn = self.driver.find_element(AppiumBy.ID, "com.plutomen.ARMS:id/btn_reg")
            rect = btn.rect
            x = rect['x'] + rect['width'] // 2
            y = rect['y'] + rect['height'] // 2
            self.driver.tap([(x, y)])
            logger.info(f"Tapped Login button coordinates at ({x}, {y})")
            return
        except Exception as e:
            logger.warning(f"Coordinate tap failed: {e}. Trying Android Enter key...")

        # Strategy 3: Android ENTER / IME Done key
        try:
            self.driver.press_keycode(66)
            logger.info("Sent KEYCODE_ENTER")
        except Exception as e:
            logger.warning(f"KEYCODE_ENTER failed: {e}")

    def click_register(self):
        """Click register/signup navigation link."""
        logger.info("Navigating to Register screen...")
        self.click(self.REGISTER_LINK, timeout=5)

    def click_forgot_password(self):
        """Click forgot password navigation link."""
        logger.info("Navigating to Forgot Password screen...")
        self.click(self.FORGOT_PASSWORD_LINK, timeout=5)

    def click_guest_login(self):
        """Click guest login navigation link."""
        logger.info("Navigating to Guest Login screen...")
        self.click(self.GUEST_LOGIN_LINK, timeout=5)

    def logout(self):
        """Execute user logout flow (Settings -> Profile -> Logout -> Confirm)."""
        logger.info("Initiating user logout...")
        # Step 1: Navigate to Settings tab if visible
        if self.is_displayed(self.SETTINGS_TAB, timeout=3):
            self.click(self.SETTINGS_TAB)
            time.sleep(1)

        # Step 2: Click Profile item if in Settings
        if self.is_displayed(self.PROFILE_ITEM, timeout=3):
            self.click(self.PROFILE_ITEM)
            time.sleep(1)

        # Step 3: Click Logout button
        if self.is_displayed(self.LOGOUT_BUTTON, timeout=3):
            self.click(self.LOGOUT_BUTTON)
            time.sleep(1)
            if self.is_displayed(self.CONFIRM_LOGOUT_BUTTON, timeout=3):
                self.click(self.CONFIRM_LOGOUT_BUTTON)
                time.sleep(2)
        else:
            # Fallback swipe to locate Logout button
            self.scroll_down()
            if self.is_displayed(self.LOGOUT_BUTTON, timeout=3):
                self.click(self.LOGOUT_BUTTON)
                time.sleep(1)
                if self.is_displayed(self.CONFIRM_LOGOUT_BUTTON, timeout=3):
                    self.click(self.CONFIRM_LOGOUT_BUTTON)
                    time.sleep(2)

    def get_error_message(self) -> str:
        """Attempt to read and dismiss any on-screen error banner, toast, or popup dialog."""
        # 1. Check and dismiss modal popup dialog first (e.g. "Server error", "Invalid credentials")
        dialog_msg = self.dismiss_popup_dialog(timeout=2)
        if dialog_msg:
            return dialog_msg

        # 2. Check for inline / toast / banner error message
        try:
            if self.is_displayed(self.ERROR_MESSAGE, timeout=2):
                return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            pass
        return ""

    def login(self, email: str, password: str):
        """Execute login flow with popup check and credential entry."""
        self.dismiss_initial_dialogs()

        if self.is_login_screen_displayed():
            logger.info("Login screen active. Submitting credentials...")
            self.enter_email(email)
            self.enter_password(password)
            self.click_login()
        elif self.is_already_logged_in():
            logger.info("Dashboard already active. User is already logged in.")
        else:
            logger.info("Attempting to locate login fields...")
            self.enter_email(email)
            self.enter_password(password)
            self.click_login()
