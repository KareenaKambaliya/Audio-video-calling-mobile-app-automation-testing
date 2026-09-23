"""
Test Suite: Create Call (Sheet: Create_Call_Test_Cases)
Data-Driven Suite for 1-on-1 Video & Audio Call Creation.
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.call_page import CallPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.adb_helper import AdbHelper
from utils.logger import logger
from config import config

SHEET_NAME = "Create_Call_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestCreateCallSuite:

    def test_create_call_scenario(self, driver, test_case):
        """Execute call creation scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_CALL")
        desc = test_case.get("Scenario_Description", "Call Creation")
        recipient = test_case.get("Recipient", "")
        call_type = test_case.get("Call_Type", "Video")
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
        call_page = CallPage(driver)
        home_page = HomePage(driver)

        # 1. Ensure user is logged in
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        # 2. Handle network condition if testing offline
        if tc_id == "TC_CALL_06":
            AdbHelper.set_wifi(False)
            AdbHelper.set_mobile_data(False)

        try:
            # 3. Start Call
            call_page.start_call(recipient=recipient, call_type=call_type)
            time.sleep(4)

            # 4. Assert Expected Result
            if expected_result == "SUCCESS":
                is_active = call_page.is_call_active() or "callactivity" in driver.current_activity.lower()
                screenshot = call_page.take_screenshot(prefix=f"PASS_{tc_id}")
                # Clean up call if active
                if call_page.is_call_active():
                    call_page.end_call()
                assert is_active, f"Expected call SUCCESS, but call did not connect. Msg: {expected_msg}"
                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot,
                    error_message=f"Call initiated successfully ({expected_msg})"
                )
            else:
                err = call_page.get_error_message()
                screenshot = call_page.take_screenshot(prefix=f"NEG_{tc_id}")
                is_blocked = not call_page.is_call_active() or bool(err)
                assert is_blocked, f"Expected call FAILURE, but call connected! Error: {err}"
                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot,
                    error_message=f"Call prevented as expected: '{err}' ({expected_msg})"
                )
        finally:
            if tc_id == "TC_CALL_06":
                # Restore network
                AdbHelper.set_wifi(True)
                AdbHelper.set_mobile_data(True)
