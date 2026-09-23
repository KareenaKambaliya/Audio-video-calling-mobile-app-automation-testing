"""
Group Chat Page Object for Plutomen Connect.
Represents GroupChatDetailsActivity, GroupInfoActivity, and group creation flows.
"""

from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class GroupChatPage(BasePage):
    """Page Object for Group Chat Management, Creation, and Group Messaging."""

    BTN_NEW_GROUP = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'New Group') or contains(@resource-id, 'btn_create_group') or "
        "contains(@resource-id, 'fab_new_group') or contains(@text, 'Create Group')]"
    )

    GROUP_NAME_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'edt_group_name') or "
        "contains(@resource-id, 'txtGroupName') or contains(@hint, 'Group Name')]"
    )

    MEMBER_CHECKBOX = (
        AppiumBy.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//*[contains(@class, 'CheckBox') or "
        "contains(@resource-id, 'cb_select') or contains(@resource-id, 'layout_contact')]"
    )

    BTN_CONFIRM_CREATE_GROUP = (
        AppiumBy.XPATH,
        "//*[(@clickable='true' or contains(@class, 'Button')) and "
        "(contains(@text, 'Create') or contains(@text, 'Done') or contains(@resource-id, 'btn_done'))]"
    )

    GROUP_TITLE_HEADER = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_group_name') or contains(@resource-id, 'txtGroupName')]"
    )

    BTN_GROUP_INFO = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'info') or contains(@resource-id, 'ic_info') or "
        "contains(@resource-id, 'iv_group_info')]"
    )

    BTN_ADD_MEMBER = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Add Member') or contains(@resource-id, 'btn_add_member')]"
    )

    BTN_REMOVE_MEMBER = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Remove') or contains(@resource-id, 'btn_remove_member')]"
    )

    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Select at least one member') or contains(@text, 'not permitted') or "
        "contains(@resource-id, 'error') or contains(@resource-id, 'snackbar')]"
    )

    def create_group(self, group_name: str, member_count: int = 1):
        """Create a new group with specified name and number of members."""
        logger.info(f"Creating group '{group_name}' with {member_count} member(s)...")
        if self.is_displayed(self.BTN_NEW_GROUP, timeout=4):
            self.click(self.BTN_NEW_GROUP)

        if group_name and self.is_displayed(self.GROUP_NAME_INPUT, timeout=4):
            self.send_keys(self.GROUP_NAME_INPUT, group_name)

        if member_count > 0:
            checkboxes = self.find_elements(self.MEMBER_CHECKBOX, timeout=4)
            for i in range(min(member_count, len(checkboxes))):
                checkboxes[i].click()

        if self.is_displayed(self.BTN_CONFIRM_CREATE_GROUP, timeout=4):
            self.click(self.BTN_CONFIRM_CREATE_GROUP)

    def is_group_created(self) -> bool:
        """Verify group conversation is open."""
        return (
            self.is_displayed(self.GROUP_TITLE_HEADER, timeout=6)
            or "groupchat" in self.get_current_activity().lower()
        )

    def open_group_info(self):
        """Navigate to Group Info screen."""
        logger.info("Opening Group Info...")
        self.click(self.BTN_GROUP_INFO, timeout=4)

    def is_group_info_displayed(self) -> bool:
        """Verify group info details are displayed."""
        return "groupinfo" in self.get_current_activity().lower() or self.is_text_present("Members", timeout=4)

    def get_error_message(self) -> str:
        """Extract visible error message."""
        try:
            if self.is_displayed(self.ERROR_MESSAGE, timeout=3):
                return self.get_text(self.ERROR_MESSAGE)
        except Exception:
            pass
        return ""
