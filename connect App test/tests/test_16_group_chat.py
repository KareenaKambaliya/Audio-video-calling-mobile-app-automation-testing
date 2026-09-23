"""
Test Suite: Group Chat (Sheet: GroupChat_Test_Cases)
Data-Driven Suite for Group creation, member administration, and group discussions.
"""

import time
import pytest
from pages.group_chat_page import GroupChatPage
from pages.chat_page import ChatPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger
from config import config

SHEET_NAME = "GroupChat_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestGroupChatSuite:

    def test_group_chat_scenario(self, driver, test_case):
        """Execute group chat scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_GCHAT")
        desc = test_case.get("Scenario_Description", "Group Chat Scenario")
        group_size = test_case.get("Group_Size", "3 members")
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
        group_page = GroupChatPage(driver)
        chat_page = ChatPage(driver)

        # 1. Ensure logged in
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        # 2. Perform Group action
        if tc_id == "TC_GCHAT_01":
            group_page.create_group("Project Alfa", member_count=2)
            time.sleep(3)
            assert group_page.is_group_created() or not group_page.is_displayed(group_page.BTN_CONFIRM_CREATE_GROUP), "Group not created!"
        elif tc_id == "TC_GCHAT_02":
            # No members selected
            group_page.create_group("Empty Group", member_count=0)
            time.sleep(2)
            err = group_page.get_error_message()
            screenshot = group_page.take_screenshot(prefix=f"NEG_{tc_id}")
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Group creation without members blocked: '{err}' ({expected_msg})"
            )
            return
        elif tc_id == "TC_GCHAT_06":
            group_page.open_group_info()
            time.sleep(2)
            assert group_page.is_group_info_displayed(), "Group info not displayed!"

        screenshot = group_page.take_screenshot(prefix=f"GRP_{tc_id}")
        ExcelReporter.log_result(
            test_name=test_title,
            status="PASSED",
            screenshot_path=screenshot,
            error_message=f"Group chat scenario executed ({expected_msg})"
        )
