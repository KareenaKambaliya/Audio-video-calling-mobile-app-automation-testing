"""
Test Suite: Guest Login (Sheet: GuestLogin_Test_Cases)
Data-Driven Suite for Guest Login and Join Code sessions.
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.guest_login_page import GuestLoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger

SHEET_NAME = "GuestLogin_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestGuestLoginSuite:

    def test_guest_login_scenario(self, driver, test_case):
        """Execute guest login scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_GUEST")
        desc = test_case.get("Scenario_Description", "Guest Login Scenario")
        guest_name = test_case.get("Guest_Name", "")
        join_code = test_case.get("Join_Code", "")
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
        guest_page = GuestLoginPage(driver)

        # 1. Dismiss popups and navigate to Guest Login
        login_page.dismiss_initial_dialogs()
        if login_page.is_already_logged_in():
            login_page.logout()
            time.sleep(2)

        if not guest_page.is_guest_login_screen_displayed():
            login_page.click_guest_login()
            time.sleep(2)

        # 2. Enter guest credentials & Join
        guest_page.login_as_guest(name=guest_name, join_code=join_code)
        time.sleep(4)

        # 3. Assert Expected Result
        if expected_result == "SUCCESS":
            is_joined = guest_page.is_joined_successfully()
            screenshot = guest_page.take_screenshot(prefix=f"PASS_{tc_id}")
            assert is_joined, f"Expected guest login SUCCESS, but session not joined. Msg: {expected_msg}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Guest login succeeded ({expected_msg})"
            )
        else:
            err = guest_page.get_error_message()
            screenshot = guest_page.take_screenshot(prefix=f"NEG_{tc_id}")
            is_blocked = guest_page.is_guest_login_screen_displayed() or bool(err)
            assert is_blocked, f"Expected guest login FAILURE, but joined session! Error: {err}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Guest login rejected as expected: '{err}' ({expected_msg})"
            )
