"""
Permissions Page Object for Plutomen Connect.
Represents ManagePermissionActivity and OS runtime permission dialogs.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class PermissionsPage(BasePage):
    """Page Object for Manage Permissions Screen and Runtime Permission Handling."""

    # --- ManagePermissionActivity Locators ---
    HEADER_MANAGE_PERMISSIONS = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Manage Permission') or contains(@text, 'Permissions')]"
    )

    BTN_OPEN_SYSTEM_SETTINGS = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Open System Permissions') or contains(@text, 'Open Settings') or "
        "contains(@resource-id, 'btn_settings') or contains(@resource-id, 'open_system_permissions')]"
    )

    CAMERA_PERM_ROW = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Camera')]/ancestor::*[contains(@class, 'RelativeLayout') or contains(@class, 'LinearLayout')][1]"
    )

    MIC_PERM_ROW = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Microphone') or contains(@text, 'Audio')]/ancestor::*[contains(@class, 'RelativeLayout') or contains(@class, 'LinearLayout')][1]"
    )

    STORAGE_PERM_ROW = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Storage')]/ancestor::*[contains(@class, 'RelativeLayout') or contains(@class, 'LinearLayout')][1]"
    )

    LOCATION_PERM_ROW = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Location')]/ancestor::*[contains(@class, 'RelativeLayout') or contains(@class, 'LinearLayout')][1]"
    )

    # --- Android OS Runtime Dialog Buttons ---
    OS_ALLOW_BUTTON = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'permission_allow_button') or "
        "contains(@resource-id, 'permission_allow_foreground_only_button') or "
        "contains(@text, 'While using the app') or contains(@text, 'Allow') or "
        "contains(@text, 'ALLOW')]"
    )

    OS_DENY_BUTTON = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'permission_deny_button') or "
        "contains(@resource-id, 'permission_deny_and_dont_ask_again_button') or "
        "contains(@text, 'Don’t allow') or contains(@text, 'Deny') or "
        "contains(@text, 'DENY')]"
    )

    def is_manage_permissions_screen_displayed(self) -> bool:
        """Verify Manage Permissions screen is active."""
        return (
            "managepermissionactivity" in self.get_current_activity().lower()
            or self.is_displayed(self.HEADER_MANAGE_PERMISSIONS, timeout=4)
        )

    def click_open_system_permissions(self):
        """Click 'Open System Permissions' button."""
        logger.info("Clicking 'Open System Permissions'...")
        self.click(self.BTN_OPEN_SYSTEM_SETTINGS, timeout=4)

    def handle_os_permission(self, action: str = "Allow"):
        """Handle OS runtime permission prompt with Allow or Deny."""
        logger.info(f"Handling runtime permission dialog with action: {action}")
        if "allow" in action.lower():
            if self.is_displayed(self.OS_ALLOW_BUTTON, timeout=3):
                self.click(self.OS_ALLOW_BUTTON)
        else:
            if self.is_displayed(self.OS_DENY_BUTTON, timeout=3):
                self.click(self.OS_DENY_BUTTON)

    def get_permission_status_text(self, permission_name: str) -> str:
        """Read displayed status (e.g. Granted or Denied) for a permission."""
        locator = (AppiumBy.XPATH, f"//*[contains(@text, '{permission_name}')]/..//*[contains(@text, 'Allow') or contains(@text, 'Den') or contains(@text, 'Grant')]")
        try:
            if self.is_displayed(locator, timeout=3):
                return self.get_text(locator)
        except Exception:
            pass
        return ""
