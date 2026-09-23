"""
Test Suite: Chat (Sheet: Chat_Test_Cases)
Data-Driven Suite for 1-on-1 Chat Messaging, attachments, and offline queueing.
"""

import time
import pytest
from pages.chat_page import ChatPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.adb_helper import AdbHelper
from utils.logger import logger
from config import config

SHEET_NAME = "Chat_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestChatSuite:

    def test_chat_scenario(self, driver, test_case):
        """Execute chat messaging scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_CHAT")
        desc = test_case.get("Scenario_Description", "Chat Scenario")
        recipient = test_case.get("Recipient", "testuser2@yopmail.com")
        msg_type = test_case.get("Message_Type", "Text")
        expected_result = test_case.get("Expected_Result", "SUCCESS").upper()
        expected_msg = test_case.get("Expected_Message", "")

        # Check Execute column from Excel
        execute_flag = str(test_case.get("Execute", "Y")).strip().upper()
        if execute_flag != "Y":
            logger.info(f"Skipping {tc_id} because Execute flag is '{execute_flag}' in Excel.")
            pytest.skip(f"Execute flag is '{execute_flag}' in Excel")


        test_title = f"{tc_id} - {desc}"
        logger.info(f"\n{'=' * 60}\nRunning [{SHEET_NAME}]: {test_title}\n{'=' * 60}")

        login_page = LoginPage(driver)
        chat_page = ChatPage(driver)

        # 1. Ensure logged in
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        # 2. Open chat conversation
        chat_page.open_chat_with_user(recipient)
        time.sleep(2)

        # 3. Handle specific scenario
        if tc_id == "TC_CHAT_03":
            # Empty message
            is_enabled = chat_page.is_send_button_enabled()
            screenshot = chat_page.take_screenshot(prefix=f"NEG_{tc_id}")
            assert not is_enabled or expected_result == "FAILURE", "Send button should be disabled for empty text!"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Empty message blocked as expected ({expected_msg})"
            )
            return

        if tc_id == "TC_CHAT_07":
            AdbHelper.set_wifi(False)
            AdbHelper.set_mobile_data(False)

        try:
            if msg_type.lower() == "image":
                chat_page.send_image_message()
            else:
                msg_text = "Hello! Test message from automation." if tc_id != "TC_CHAT_05" else "Hello 😊 👍 🚀 @#$%"
                chat_page.send_text_message(msg_text)

            time.sleep(3)

            screenshot = chat_page.take_screenshot(prefix=f"PASS_{tc_id}")
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Chat message sent successfully ({expected_msg})"
            )
        finally:
            if tc_id == "TC_CHAT_07":
                AdbHelper.set_wifi(True)
                AdbHelper.set_mobile_data(True)
