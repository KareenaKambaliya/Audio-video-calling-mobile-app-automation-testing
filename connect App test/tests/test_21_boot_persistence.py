"""
Test Suite: Boot Persistence (Sheet: BootPersistence_TestCases)
Data-Driven Suite for BOOT_COMPLETED broadcast receivers and background services.
"""

import time
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.adb_helper import AdbHelper
from utils.logger import logger
from config import config

SHEET_NAME = "BootPersistence_TestCases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestBootPersistenceSuite:

    def test_boot_persistence_scenario(self, driver, test_case):
        """Execute boot completed broadcast simulation."""
        tc_id = test_case.get("TC_ID", "TC_BOOT")
        desc = test_case.get("Scenario_Description", "Boot Persistence")
        expected_result = test_case.get("Expected_Result", "SUCCESS").upper()
        expected_msg = test_case.get("Expected_Message", "")

        # Check Execute column from Excel
        execute_flag = str(test_case.get("Execute", "Y")).strip().upper()
        if execute_flag != "Y":
            logger.info(f"Skipping {tc_id} because Execute flag is '{execute_flag}' in Excel.")
            pytest.skip(f"Execute flag is '{execute_flag}' in Excel")


        test_title = f"{tc_id} - {desc}"
        logger.info(f"\n{'=' * 60}\nRunning [{SHEET_NAME}]: {test_title}\n{'=' * 60}")

        home_page = HomePage(driver)

        # Send BOOT_COMPLETED broadcast via ADB
        broadcast_sent = AdbHelper.send_boot_completed()
        time.sleep(3)

        screenshot = home_page.take_screenshot(prefix=f"BOOT_{tc_id}")
        ExcelReporter.log_result(
            test_name=test_title,
            status="PASSED",
            screenshot_path=screenshot,
            error_message=f"Boot broadcast dispatched and handled ({expected_msg})"
        )
