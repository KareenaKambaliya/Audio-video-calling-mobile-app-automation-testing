"""
Test Suite: User Registration (Sheet: Register_Test_Cases)
Data-Driven Suite for Plutomen Connect Account Registration flows.
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger

SHEET_NAME = "Register_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestRegisterSuite:

    def test_registration_scenario(self, driver, test_case):
        """Execute user registration scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_REG")
        desc = test_case.get("Scenario_Description", "Registration Scenario")
        name = test_case.get("Name", "")
        email = test_case.get("Email", "")
        password = test_case.get("Password", "")
        confirm_password = test_case.get("Confirm_Password", "")
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
        register_page = RegisterPage(driver)

        # 1. Dismiss initial popups and navigate to register
        login_page.dismiss_initial_dialogs()
        if login_page.is_already_logged_in():
            login_page.logout()
            time.sleep(2)

        if not register_page.is_register_screen_displayed():
            login_page.click_register()
            time.sleep(2)

        # 2. Fill form and submit
        register_page.fill_registration_form(name, email, password, confirm_password)
        register_page.click_register()
        time.sleep(3)

        # 3. Assert Expected Result
        if expected_result == "SUCCESS":
            is_success = register_page.is_registration_successful()
            screenshot = register_page.take_screenshot(prefix=f"PASS_{tc_id}")
            assert is_success, f"Expected registration SUCCESS, but not confirmed. Msg: {expected_msg}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Registration succeeded ({expected_msg})"
            )
        else:
            err = register_page.get_error_message()
            screenshot = register_page.take_screenshot(prefix=f"NEG_{tc_id}")
            is_blocked = register_page.is_register_screen_displayed() or bool(err)
            assert is_blocked, f"Expected registration FAILURE, but proceeded! Error: {err}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Registration blocked as expected: '{err}' ({expected_msg})"
            )
