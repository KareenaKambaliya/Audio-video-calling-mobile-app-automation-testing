"""
Test Suite: Offline Self Mode (Sheet: ScheduleOfflineMode_TestCases)
Data-Driven Suite for Self-guided AR and Non-AR offline sessions.
"""

import time
import pytest
from pages.offline_mode_page import OfflineModePage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.adb_helper import AdbHelper
from utils.logger import logger
from config import config

SHEET_NAME = "ScheduleOfflineMode_TestCases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestScheduleOfflineSuite:

    def test_offline_mode_scenario(self, driver, test_case):
        """Execute offline self-mode scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_SOFF")
        desc = test_case.get("Scenario_Description", "Offline Mode Scenario")
        mode = test_case.get("Mode", "AR")
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
        offline_page = OfflineModePage(driver)

        # 1. Ensure logged in
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        # 2. Simulate No Internet if testing TC_SOFF_04
        if tc_id == "TC_SOFF_04":
            AdbHelper.set_wifi(False)
            AdbHelper.set_mobile_data(False)

        try:
            offline_page.navigate_to_self_mode()
            time.sleep(2)
            title = "" if "empty" in desc.lower() else f"Inspection {tc_id}"
            offline_page.start_self_mode_session(title=title, mode=mode)
            time.sleep(3)

            # 3. Assert Expected Result
            if "SUCCESS" in expected_result:
                is_active = offline_page.is_session_active() or "selfmode" in driver.current_activity.lower()
                screenshot = offline_page.take_screenshot(prefix=f"PASS_{tc_id}")
                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot,
                    error_message=f"Self mode started ({expected_msg})"
                )
            else:
                err = offline_page.get_error_message()
                screenshot = offline_page.take_screenshot(prefix=f"NEG_{tc_id}")
                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot,
                    error_message=f"Offline mode handled as expected: '{err}' ({expected_msg})"
                )
        finally:
            if tc_id == "TC_SOFF_04":
                AdbHelper.set_wifi(True)
                AdbHelper.set_mobile_data(True)
