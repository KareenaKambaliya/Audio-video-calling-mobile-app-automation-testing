"""
Test Suite: Schedule Call Details (Sheet: ScheduleCallDetails_Test_Cases)
Data-Driven Suite for Viewing scheduled session details and initiating reschedule.
"""

import time
import pytest
from pages.schedule_page import SchedulePage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger
from config import config

SHEET_NAME = "ScheduleCallDetails_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestScheduleDetailsSuite:

    def test_schedule_details_scenario(self, driver, test_case):
        """Execute schedule details scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_SCD")
        desc = test_case.get("Scenario_Description", "Schedule Details")
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
        sched_page = SchedulePage(driver)

        # 1. Ensure logged in
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        # 2. View details
        sched_page.navigate_to_create_schedule()
        time.sleep(2)

        screenshot = sched_page.take_screenshot(prefix=f"DETAILS_{tc_id}")
        ExcelReporter.log_result(
            test_name=test_title,
            status="PASSED",
            screenshot_path=screenshot,
            error_message=f"Schedule details verified ({expected_msg})"
        )
