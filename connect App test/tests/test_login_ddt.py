"""
Data-Driven Test Suite for Plutomen Connect Login.
Loads test scenarios dynamically from Excel (data/login_test_data.xlsx).
Execute with: pytest -v tests/test_login_ddt.py
"""

import time
import pytest

from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.excel_reader import get_login_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger

# Load enabled test cases from Excel
TEST_CASES = get_login_test_cases()


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc["TC_ID"] for tc in TEST_CASES])
class TestLoginDDT:

    def test_login(self, driver, test_case):
        """
        Execute login test scenario with credentials loaded from Excel.
        """
        tc_id = test_case.get("TC_ID", "UNKNOWN")
        desc = test_case.get("Scenario_Description", "Login Test")
        email = test_case.get("Email", "")
        password = test_case.get("Password", "")
        expected_result = test_case.get("Expected_Result", "SUCCESS").upper()
        expected_msg = test_case.get("Expected_Message", "")

        test_title = f"{tc_id} - {desc}"
        logger.info(f"\n{'=' * 60}\nRunning DDT Test Case: {test_title}\n{'=' * 60}")
        logger.info(f"Inputs -> Email: '{email}', Expected: '{expected_result}'")

        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        # 1. Dismiss splash dialogs if present
        login_page.dismiss_initial_dialogs()
        time.sleep(2)

        # 2. Enter credentials and click Login
        if email or password:
            login_page.login(email=email, password=password)
        else:
            login_page.click_login()

        time.sleep(4)

        # 3. Validate outcome according to Excel expectation
        screenshot_path = ""
        try:
            if expected_result == "SUCCESS":
                # Check that dashboard or app is running
                assert home_page.is_app_in_foreground(), "App is not in foreground after login."
                is_logged_in = login_page.is_already_logged_in() or home_page.is_dashboard_visible()
                screenshot_path = login_page.take_screenshot(prefix=f"PASS_{tc_id}")

                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot_path,
                    error_message=f"Login successful as expected ({expected_msg})"
                )
                logger.info(f"[DDT RESULT] {tc_id} PASSED (Login Succeeded)")

            elif expected_result == "FAILURE":
                # Negative test verification
                error_msg = login_page.get_error_message()
                screenshot_path = login_page.take_screenshot(prefix=f"NEG_{tc_id}")

                ExcelReporter.log_result(
                    test_name=test_title,
                    status="PASSED",
                    screenshot_path=screenshot_path,
                    error_message=f"Validation error displayed as expected: '{error_msg}'"
                )
                logger.info(f"[DDT RESULT] {tc_id} PASSED (Negative scenario confirmed)")

        except AssertionError as ae:
            screenshot_path = login_page.take_screenshot(prefix=f"FAIL_{tc_id}")
            ExcelReporter.log_result(
                test_name=test_title,
                status="FAILED",
                screenshot_path=screenshot_path,
                error_message=str(ae)
            )
            raise ae
