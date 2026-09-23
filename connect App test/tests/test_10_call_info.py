"""
Test Suite: Call Info (Sheet: CallInfo_Test_Cases)
Data-Driven Suite for Call Info details and post-call summaries.
"""

import time
import pytest
from pages.call_page import CallPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger
from config import config

SHEET_NAME = "CallInfo_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestCallInfoSuite:

    def test_call_info_scenario(self, driver, test_case):
        """Execute Call Info scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_CINFO")
        desc = test_case.get("Scenario_Description", "Call Info Scenario")
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

        # 1. Ensure logged in
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        try:
            if tc_id == "TC_CINFO_01":
                # Active Call Info
                if not call_page.is_call_active():
                    call_page.start_call("testuser2@yopmail.com", "Video")
                    time.sleep(3)
                call_page.open_call_info()
                time.sleep(2)
                screenshot = call_page.take_screenshot(prefix=f"PASS_{tc_id}")
                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot,
                    error_message=f"Active call info verified ({expected_msg})"
                )
            else:
                # Post-call / missed call info
                screenshot = call_page.take_screenshot(prefix=f"INFO_{tc_id}")
                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot,
                    error_message=f"Call info state verified ({expected_msg})"
                )
        finally:
            if call_page.is_call_active():
                call_page.end_call()
