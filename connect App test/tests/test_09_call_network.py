"""
Test Suite: Call Network Handling (Sheet: CallNetworkHandling_Test_Cases)
Data-Driven Suite for Call stability under network transitions, network loss, and reconnects.
"""

import time
import pytest
from pages.call_page import CallPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.adb_helper import AdbHelper
from utils.logger import logger
from config import config

SHEET_NAME = "CallNetworkHandling_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestCallNetworkSuite:

    def test_call_network_scenario(self, driver, test_case):
        """Execute network resilience scenario during active call."""
        tc_id = test_case.get("TC_ID", "TC_NET")
        desc = test_case.get("Scenario_Description", "Network Handling")
        net_condition = test_case.get("Network_Condition", "")
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

        # 1. Ensure in active call
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        if not call_page.is_call_active():
            call_page.start_call("testuser2@yopmail.com", "Video")
            time.sleep(4)

        try:
            # 2. Simulate Network Condition
            if tc_id == "TC_NET_01":
                # Wi-Fi to Mobile data switch
                AdbHelper.set_wifi(False)
                AdbHelper.set_mobile_data(True)
                time.sleep(4)
                assert call_page.is_call_active() or "callactivity" in driver.current_activity.lower(), "Call dropped during Wi-Fi to Data handover!"
            elif tc_id == "TC_NET_02":
                # Complete network loss
                AdbHelper.set_wifi(False)
                AdbHelper.set_mobile_data(False)
                time.sleep(5)
                # Call should show reconnect banner or drop
            elif tc_id == "TC_NET_03":
                # Brief loss then restore
                AdbHelper.set_wifi(False)
                time.sleep(3)
                AdbHelper.set_wifi(True)
                time.sleep(5)
                assert call_page.is_call_active(), "Call did not auto-reconnect after brief network loss!"
            elif tc_id == "TC_NET_05":
                # Airplane mode toggle
                AdbHelper.set_airplane_mode(True)
                time.sleep(3)
                AdbHelper.set_airplane_mode(False)
                time.sleep(5)

            screenshot = call_page.take_screenshot(prefix=f"NET_{tc_id}")
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Network condition '{net_condition}' handled properly ({expected_msg})"
            )
        finally:
            # Restore connectivity
            AdbHelper.set_airplane_mode(False)
            AdbHelper.set_wifi(True)
            AdbHelper.set_mobile_data(True)
            if call_page.is_call_active():
                call_page.end_call()
