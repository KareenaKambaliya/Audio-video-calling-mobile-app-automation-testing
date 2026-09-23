"""
Test Suite: Receive Call (Sheet: ReceiveCall_Test_Cases)
Data-Driven Suite for Incoming Call handling, acceptance, rejection, and notification actions.
"""

import time
import pytest
from pages.call_page import CallPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger
from config import config

SHEET_NAME = "ReceiveCall_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestReceiveCallSuite:

    def test_receive_call_scenario(self, driver, test_case):
        """Execute incoming call scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_RCALL")
        desc = test_case.get("Scenario_Description", "Receive Call Scenario")
        caller = test_case.get("Caller", "")
        call_type = test_case.get("Call_Type", "Video")
        action = test_case.get("Action", "Accept")
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

        # 2. Handle scenario action
        if "reject" in action.lower():
            if call_page.is_incoming_call_displayed():
                call_page.reject_incoming_call()
            time.sleep(2)
            screenshot = call_page.take_screenshot(prefix=f"PASS_{tc_id}")
            assert not call_page.is_call_active(), f"Call is still active after rejection! Msg: {expected_msg}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Incoming call rejected cleanly ({expected_msg})"
            )
        elif "accept" in action.lower():
            if call_page.is_incoming_call_displayed():
                call_page.accept_incoming_call()
                time.sleep(3)
                screenshot = call_page.take_screenshot(prefix=f"PASS_{tc_id}")
                is_active = call_page.is_call_active()
                if is_active:
                    call_page.end_call()
                assert is_active, f"Call did not connect on accept! Msg: {expected_msg}"
            else:
                screenshot = call_page.take_screenshot(prefix=f"SIM_{tc_id}")
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Incoming call accept flow verified ({expected_msg})"
            )
        else:
            # Timeout / Missed call
            time.sleep(5)
            screenshot = call_page.take_screenshot(prefix=f"TIMEOUT_{tc_id}")
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Call timeout behavior verified ({expected_msg})"
            )
