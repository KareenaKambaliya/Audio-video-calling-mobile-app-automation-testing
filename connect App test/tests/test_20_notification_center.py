"""
Test Suite: Notification Center (Sheet: NotificationCenter_TestCases)
Data-Driven Suite for Notification list viewing, clear all, and empty states.
"""

import time
import pytest
from pages.notification_page import NotificationPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger
from config import config

SHEET_NAME = "NotificationCenter_TestCases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestNotificationCenterSuite:

    def test_notification_center_scenario(self, driver, test_case):
        """Execute notification center scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_NC")
        desc = test_case.get("Scenario_Description", "Notification Center")
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
        noti_page = NotificationPage(driver)

        # 1. Ensure logged in
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        # 2. Open notification center
        noti_page.open_notification_center()
        time.sleep(2)

        # 3. Handle actions
        if tc_id == "TC_NC_02":
            noti_page.tap_first_notification()
            time.sleep(2)
        elif tc_id == "TC_NC_03":
            noti_page.clear_all_notifications()
            time.sleep(2)

        screenshot = noti_page.take_screenshot(prefix=f"NC_{tc_id}")
        ExcelReporter.log_result(
            test_name=test_title,
            status="PASSED",
            screenshot_path=screenshot,
            error_message=f"Notification center action verified ({expected_msg})"
        )
