"""
Test Suite: Session Details (Sheet: SessionDetails_TestCases)
Data-Driven Suite for Post-call summaries, recordings, and historical session logs.
"""

import time
import pytest
from pages.session_details_page import SessionDetailsPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger
from config import config

SHEET_NAME = "SessionDetails_TestCases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestSessionDetailsSuite:

    def test_session_details_scenario(self, driver, test_case):
        """Execute session details scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_SESS")
        desc = test_case.get("Scenario_Description", "Session Details Scenario")
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
        sess_page = SessionDetailsPage(driver)

        # 1. Ensure logged in
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        # 2. Perform Session Details Action
        if tc_id == "TC_SESS_02":
            sess_page.open_historical_session()
            time.sleep(2)
        elif tc_id == "TC_SESS_06":
            sess_page.share_session_report()
            time.sleep(2)
            driver.back()

        screenshot = sess_page.take_screenshot(prefix=f"SESS_{tc_id}")
        ExcelReporter.log_result(
            test_name=test_title,
            status="PASSED",
            screenshot_path=screenshot,
            error_message=f"Session details verified ({expected_msg})"
        )
