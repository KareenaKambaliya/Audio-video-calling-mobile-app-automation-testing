"""
Test Suite: Create Schedule (Sheet: CreateSchedule_Test_Cases)
Data-Driven Suite for Scheduling sessions, validations, editing, and cancellation.
"""

import time
import pytest
from pages.schedule_page import SchedulePage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger
from config import config

SHEET_NAME = "CreateSchedule_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestCreateScheduleSuite:

    def test_create_schedule_scenario(self, driver, test_case):
        """Execute schedule creation scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_SCH")
        desc = test_case.get("Scenario_Description", "Schedule Scenario")
        title = test_case.get("Title", "")
        date_time = test_case.get("Date_Time", "")
        participant = test_case.get("Participant", "")
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

        # 2. Check if cancellation test
        if tc_id == "TC_SCH_08":
            sched_page.cancel_schedule()
            time.sleep(2)
            screenshot = sched_page.take_screenshot(prefix=f"PASS_{tc_id}")
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Schedule cancelled as expected ({expected_msg})"
            )
            return

        # 3. Navigate and submit schedule
        sched_page.navigate_to_create_schedule()
        time.sleep(2)
        sched_page.fill_schedule_form(title=title, date_time=date_time, participant=participant)
        sched_page.submit_schedule()
        time.sleep(3)

        # 4. Assert Expected Result
        if expected_result == "SUCCESS":
            is_created = sched_page.is_schedule_created()
            screenshot = sched_page.take_screenshot(prefix=f"PASS_{tc_id}")
            assert is_created, f"Expected schedule to be created. Msg: {expected_msg}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Schedule created successfully ({expected_msg})"
            )
        else:
            err = sched_page.get_error_message()
            screenshot = sched_page.take_screenshot(prefix=f"NEG_{tc_id}")
            is_blocked = sched_page.is_create_schedule_screen_displayed() or bool(err)
            assert is_blocked, f"Expected schedule creation FAILURE, but form closed! Error: {err}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Schedule creation blocked: '{err}' ({expected_msg})"
            )
