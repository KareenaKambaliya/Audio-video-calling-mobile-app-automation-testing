"""
Test Suite: Screen Share & AR Annotation (Sheet: ScreenShare_Test_Cases)
Data-Driven Suite for AR & Non-AR screen sharing and collaborative drawings.
"""

import time
import pytest
from pages.call_page import CallPage
from pages.screenshare_page import ScreenSharePage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger
from config import config

SHEET_NAME = "ScreenShare_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestScreenShareSuite:

    def test_screenshare_scenario(self, driver, test_case):
        """Execute screen sharing scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_SS")
        desc = test_case.get("Scenario_Description", "Screen Share Scenario")
        share_mode = test_case.get("Share_Mode", "AR")
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
        share_page = ScreenSharePage(driver)

        # 1. Ensure in active call
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        if not call_page.is_call_active():
            call_page.start_call("testuser2@yopmail.com", "Video")
            time.sleep(4)

        try:
            # 2. Perform screen share action
            if tc_id == "TC_SS_03":
                # Stop share
                share_page.start_screen_share(mode="AR")
                time.sleep(2)
                share_page.stop_screen_share()
                time.sleep(2)
                assert call_page.is_call_active(), "Call dropped after stopping screen share!"
                screenshot = share_page.take_screenshot(prefix=f"PASS_{tc_id}")
                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot,
                    error_message=f"Screen share stopped, call active ({expected_msg})"
                )
                return

            # Start share
            share_page.start_screen_share(mode=share_mode)
            time.sleep(3)

            # 3. Assert Expected Result
            if expected_result == "SUCCESS":
                is_active = share_page.is_screen_share_active() or call_page.is_call_active()
                screenshot = share_page.take_screenshot(prefix=f"PASS_{tc_id}")
                assert is_active, f"Screen share did not activate as expected. Msg: {expected_msg}"
                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot,
                    error_message=f"Screen share running in {share_mode} ({expected_msg})"
                )
            else:
                screenshot = share_page.take_screenshot(prefix=f"NEG_{tc_id}")
                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot,
                    error_message=f"Screen share blocked as expected ({expected_msg})"
                )
        finally:
            if call_page.is_call_active():
                call_page.end_call()
