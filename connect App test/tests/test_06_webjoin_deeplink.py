"""
Test Suite: Web Join & Deep Linking (Sheet: WebJoinDeepLink_Test_Cases)
Data-Driven Suite for Deep Link Session Joining.
"""

import time
import pytest
from pages.webjoin_page import WebJoinPage
from pages.home_page import HomePage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.adb_helper import AdbHelper
from utils.logger import logger

SHEET_NAME = "WebJoinDeepLink_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestWebJoinDeepLinkSuite:

    def test_deeplink_scenario(self, driver, test_case):
        """Execute deep-link join scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_WJ")
        desc = test_case.get("Scenario_Description", "Deep Link Join")
        link_type = test_case.get("Link_Type", "")
        expected_result = test_case.get("Expected_Result", "SUCCESS").upper()
        expected_msg = test_case.get("Expected_Message", "")

        # Check Execute column from Excel
        execute_flag = str(test_case.get("Execute", "Y")).strip().upper()
        if execute_flag != "Y":
            logger.info(f"Skipping {tc_id} because Execute flag is '{execute_flag}' in Excel.")
            pytest.skip(f"Execute flag is '{execute_flag}' in Excel")


        test_title = f"{tc_id} - {desc}"
        logger.info(f"\n{'=' * 60}\nRunning [{SHEET_NAME}]: {test_title}\n{'=' * 60}")

        webjoin_page = WebJoinPage(driver)
        home_page = HomePage(driver)

        # 1. Fire intent via ADB
        AdbHelper.launch_deep_link(link_type)
        time.sleep(4)

        # 2. Assert Outcome
        if expected_result == "SUCCESS":
            is_active = webjoin_page.is_join_screen_displayed()
            screenshot = webjoin_page.take_screenshot(prefix=f"PASS_{tc_id}")
            assert is_active, f"Expected Join screen to open from deep link. Msg: {expected_msg}"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Deep link opened join screen successfully ({expected_msg})"
            )
        else:
            # Failure / graceful handling / expired
            screenshot = webjoin_page.take_screenshot(prefix=f"NEG_{tc_id}")
            status_msg = webjoin_page.get_status_or_error_message()
            # App must still be alive and either showing error or staying safe
            assert home_page.is_app_in_foreground(), "App crashed on invalid/expired deep link!"
            ExcelReporter.log_result(
                test_name=test_title,
                status="PASSED",
                screenshot_path=screenshot,
                error_message=f"Deep link handled safely: '{status_msg}' ({expected_msg})"
            )
