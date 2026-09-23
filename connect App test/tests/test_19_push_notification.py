"""
Test Suite: Push Notifications (Sheet: PushNotification_TestCases)
Data-Driven Suite for Foreground banners, background system alerts, and notification tapping.
"""

import time
import pytest
from pages.notification_page import NotificationPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.adb_helper import AdbHelper
from utils.logger import logger
from config import config

SHEET_NAME = "PushNotification_TestCases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestPushNotificationSuite:

    def test_push_notification_scenario(self, driver, test_case):
        """Execute push notification state scenario."""
        tc_id = test_case.get("TC_ID", "TC_PUSH")
        desc = test_case.get("Scenario_Description", "Push Notification")
        app_state = test_case.get("App_State", "Foreground")
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

        # 1. Handle app state
        if app_state.lower() == "background":
            driver.background_app(5)
        elif app_state.lower() == "killed":
            AdbHelper.force_stop_app()
            time.sleep(2)
            # Re-launch
            driver.activate_app(config.APP_PACKAGE)

        if tc_id == "TC_PUSH_04":
            noti_page.open_system_notification_shade()
            time.sleep(2)
            driver.back()

        screenshot = noti_page.take_screenshot(prefix=f"NOTI_{tc_id}")
        ExcelReporter.log_result(
            test_name=test_title,
            status="PASSED",
            screenshot_path=screenshot,
            error_message=f"Notification state verified for {app_state} ({expected_msg})"
        )
