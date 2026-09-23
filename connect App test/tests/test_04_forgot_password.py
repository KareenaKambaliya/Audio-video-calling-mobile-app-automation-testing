"""
Test Suite: Forgot Password (Sheet: ForgotPassword_Test_Cases)
Data-Driven Suite for Password Reset requests.
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger

SHEET_NAME = "ForgotPassword_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestForgotPasswordSuite:

    def test_forgot_password_scenario(self, driver, test_case):
        """Execute forgot password test scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_FP")
        desc = test_case.get("Scenario_Description", "Forgot Password Scenario")
        email = test_case.get("Email", "")
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
        fp_page = ForgotPasswordPage(driver)

        # 1. Dismiss dialogs and navigate to forgot password
        login_page.dismiss_initial_dialogs()
        if login_page.is_already_logged_in():
            login_page.logout()
            time.sleep(2)

        if not fp_page.is_forgot_password_screen_displayed():
            login_page.click_forgot_password()
            time.sleep(2)

        # 2. Submit request
        fp_page.request_password_reset(email)
        time.sleep(3)

        # 3. Assert Expected Result
        if expected_result == "SUCCESS":
            is_sent = fp_page.is_reset_email_sent() or not fp_page.is_forgot_password_screen_displayed()
            screenshot = fp_page.take_screenshot(prefix=f"PASS_{tc_id}")
            assert is_sent, f"Expected password reset SUCCESS, but confirmation not seen. Msg: {expected_msg}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Password reset link sent ({expected_msg})"
            )
        else:
            err = fp_page.get_error_message()
            screenshot = fp_page.take_screenshot(prefix=f"NEG_{tc_id}")
            is_blocked = fp_page.is_forgot_password_screen_displayed() or bool(err)
            assert is_blocked, f"Expected reset FAILURE, but request succeeded! Error: {err}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Reset blocked as expected: '{err}' ({expected_msg})"
            )
