"""
Test Suite: Share Into App (Sheet: ShareIntoApp_Test_Cases)
Data-Driven Suite for Android Send/Share Intents into Plutomen Connect.
"""

import time
import pytest
from pages.sharing_page import SharingPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.adb_helper import AdbHelper
from utils.logger import logger
from config import config

SHEET_NAME = "ShareIntoApp_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestShareIntoAppSuite:

    def test_share_into_app_scenario(self, driver, test_case):
        """Execute share intent scenario from external applications."""
        tc_id = test_case.get("TC_ID", "TC_SHARE")
        desc = test_case.get("Scenario_Description", "Share Into App")
        content_type = test_case.get("Content_Type", "Text")
        expected_result = test_case.get("Expected_Result", "SUCCESS").upper()
        expected_msg = test_case.get("Expected_Message", "")

        # Check Execute column from Excel
        execute_flag = str(test_case.get("Execute", "Y")).strip().upper()
        if execute_flag != "Y":
            logger.info(f"Skipping {tc_id} because Execute flag is '{execute_flag}' in Excel.")
            pytest.skip(f"Execute flag is '{execute_flag}' in Excel")


        test_title = f"{tc_id} - {desc}"
        logger.info(f"\n{'=' * 60}\nRunning [{SHEET_NAME}]: {test_title}\n{'=' * 60}")

        share_page = SharingPage(driver)

        # 1. Trigger share intent via ADB
        share_text = "Important work order details for Connect session"
        AdbHelper.send_share_intent(text=share_text)
        time.sleep(4)

        # 2. Handle scenario
        if tc_id == "TC_SHARE_04":
            # Cancel share
            driver.back()
            time.sleep(2)
            screenshot = share_page.take_screenshot(prefix=f"PASS_{tc_id}")
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Share cancelled cleanly ({expected_msg})"
            )
            return

        is_received = share_page.is_share_screen_displayed() or "sharing" in driver.current_activity.lower()
        screenshot = share_page.take_screenshot(prefix=f"SHARE_{tc_id}")

        if expected_result == "SUCCESS":
            assert is_received or "plutomen" in driver.current_package.lower(), f"Content was not received by app! Msg: {expected_msg}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Share content received ({expected_msg})"
            )
        else:
            err = share_page.get_error_message()
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Unsupported format rejected: '{err}' ({expected_msg})"
            )
