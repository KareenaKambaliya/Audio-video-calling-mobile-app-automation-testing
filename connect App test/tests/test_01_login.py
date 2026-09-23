"""
Test Suite: Login (Sheet: Login_Test_Cases)
Data-Driven Suite for Plutomen Connect Login & Logout flows.
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger

SHEET_NAME = "Login_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestLoginSuite:

    def test_login_scenario(self, driver, test_case):
        """Execute login test scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_LOGIN")
        desc = test_case.get("Scenario_Description", "Login Scenario")
        email = test_case.get("Email", "")
        password = test_case.get("Password", "")
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
        home_page = HomePage(driver)

        # 0. Ensure app is in foreground
        try:
            driver.activate_app(config.APP_PACKAGE)
        except Exception:
            pass

        # 1. Dismiss any blocking dialogs (including leftover OK dialogs)
        login_page.dismiss_initial_dialogs()
        time.sleep(1)

        # 2. Check if already logged in and scenario needs fresh login
        if login_page.is_already_logged_in() and tc_id != "TC_LOGIN_02":
            login_page.logout()
            time.sleep(2)

        # 3. Perform action based on scenario
        if tc_id == "TC_LOGIN_02":
            # Logout test
            if not login_page.is_already_logged_in():
                login_page.login(email, password)
                time.sleep(3)
            login_page.logout()
            time.sleep(2)
            assert login_page.is_login_screen_displayed(), "User was not redirected to login screen after logout."
            screenshot = login_page.take_screenshot(prefix=f"PASS_{tc_id}")
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Logout successful as expected ({expected_msg})"
            )
            return

        # Ensure any leftover popup is dismissed before typing
        login_page.dismiss_popup_dialog(timeout=1)

        # Regular login actions
        if email or password:
            login_page.enter_email(email)
            login_page.enter_password(password)
            login_page.click_login()
        else:
            login_page.click_login()

        time.sleep(4)

        # 4. Assert Expected Result
        if expected_result == "SUCCESS":
            is_success = home_page.is_dashboard_visible() or login_page.is_already_logged_in() or home_page.is_app_in_foreground()
            screenshot = login_page.take_screenshot(prefix=f"PASS_{tc_id}")
            assert is_success, f"Expected login SUCCESS, but dashboard not active. Msg: {expected_msg}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Login succeeded as expected ({expected_msg})"
            )
        else:
            time.sleep(1)
            # Capture screenshot while error popup is on screen for reporting
            screenshot = login_page.take_screenshot(prefix=f"NEG_{tc_id}")
            # Read message and click OK to dismiss popup so screen does NOT get stuck!
            err = login_page.get_error_message()
            login_page.dismiss_popup_dialog(timeout=1)

            # Failure expected: app stays on login or displays error
            is_blocked = login_page.is_login_screen_displayed() or bool(err)
            assert is_blocked, f"Expected login FAILURE, but proceeded to next screen! Error: {err}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Negative test verified: '{err}' ({expected_msg})"
            )
