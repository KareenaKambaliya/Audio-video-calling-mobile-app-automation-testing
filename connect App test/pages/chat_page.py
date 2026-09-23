"""
Chat Page Object for Plutomen Connect.
Represents com.plutomen.ARMS.activity.ChatDetailsActivity.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from core.base_page import BasePage
from utils.logger import logger


class ChatPage(BasePage):
    """Page Object for 1-on-1 Chat Messaging and Media Attachment."""

    TAB_CHATS = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Chat') or contains(@text, 'Chats') or contains(@resource-id, 'chat_tab')]"
    )

    SEARCH_CHAT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'search') or contains(@hint, 'Search')]"
    )

    CHAT_CONTACT_ITEM = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'tv_name') or contains(@resource-id, 'txtUserName') or "
        "contains(@resource-id, 'layout_chat_item')]"
    )

    # --- Chat Details Screen Locators ---
    MESSAGE_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@resource-id, 'edt_msg') or contains(@resource-id, 'et_message') or "
        "contains(@hint, 'Type a message') or contains(@hint, 'Message') or contains(@resource-id, 'edtMessage')]"
    )

    BTN_SEND = (
        AppiumBy.XPATH,
        "//*[(@clickable='true' or contains(@class, 'ImageView')) and "
        "(contains(@resource-id, 'btn_send') or contains(@resource-id, 'ivSend') or "
        "contains(@resource-id, 'send') or contains(@content-desc, 'Send'))]"
    )

    BTN_ATTACHMENT = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'attachment') or contains(@resource-id, 'icn_attachment') or "
        "contains(@resource-id, 'ivAttachment') or contains(@content-desc, 'Attach')]"
    )

    OPTION_ATTACH_IMAGE = (
        AppiumBy.XPATH,
        "//*[contains(@text, 'Gallery') or contains(@resource-id, 'icn_chat_gallery') or "
        "contains(@resource-id, 'll_gallery')]"
    )

    FIRST_GALLERY_IMAGE = (
        AppiumBy.XPATH,
        "//androidx.recyclerview.widget.RecyclerView//*[contains(@class, 'ImageView')]"
    )

    LAST_SENT_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'bgchatsender') or contains(@resource-id, 'tv_sender_message') or "
        "contains(@resource-id, 'txtMessage')]"
    )

    ERROR_MESSAGE = (
        AppiumBy.XPATH,
        "//*[contains(@resource-id, 'error') or contains(@resource-id, 'snackbar') or "
        "contains(@resource-id, 'tv_msg')]"
    )

    def open_chat_with_user(self, recipient: str):
        """Find contact and open chat conversation."""
        logger.info(f"Opening chat conversation with '{recipient}'...")
        if self.is_displayed(self.TAB_CHATS, timeout=3):
            self.click(self.TAB_CHATS)

        if recipient and self.is_displayed(self.SEARCH_CHAT, timeout=3):
            self.send_keys(self.SEARCH_CHAT, recipient)
            time.sleep(1)

        if self.is_displayed(self.CHAT_CONTACT_ITEM, timeout=4):
            self.click(self.CHAT_CONTACT_ITEM)

    def is_chat_screen_displayed(self) -> bool:
        """Verify chat conversation screen is active."""
        return (
            self.is_displayed(self.MESSAGE_INPUT, timeout=5)
            or "chatdetailsactivity" in self.get_current_activity().lower()
        )

    def enter_message(self, message: str):
        """Type message into input field."""
        logger.info(f"Typing message: '{message}'")
        self.send_keys(self.MESSAGE_INPUT, message, timeout=4)

    def click_send(self):
        """Click send button."""
        logger.info("Clicking Send message...")
        self.click(self.BTN_SEND, timeout=4)

    def send_text_message(self, text: str):
        """Complete flow of typing and sending message."""
        self.enter_message(text)
        self.click_send()

    def send_image_message(self):
        """Attach and send an image from gallery."""
        logger.info("Attaching image to chat...")
        if self.is_displayed(self.BTN_ATTACHMENT, timeout=4):
            self.click(self.BTN_ATTACHMENT)
            if self.is_displayed(self.OPTION_ATTACH_IMAGE, timeout=3):
                self.click(self.OPTION_ATTACH_IMAGE)
                if self.is_displayed(self.FIRST_GALLERY_IMAGE, timeout=4):
                    self.click(self.FIRST_GALLERY_IMAGE)
                    if self.is_displayed(self.BTN_SEND, timeout=3):
                        self.click(self.BTN_SEND)

    def is_send_button_enabled(self) -> bool:
        """Check if send button is enabled for interaction."""
        try:
            elem = self.find_element(self.BTN_SEND, timeout=3)
            return elem.is_enabled()
        except Exception:
            return False

    def is_message_delivered(self) -> bool:
        """Verify message delivery bubble appears."""
        return self.is_displayed(self.LAST_SENT_MESSAGE, timeout=6)
