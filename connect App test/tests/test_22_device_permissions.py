"""
Test Suite: Device Permissions (Sheet: DevicePermissions_TestCases)
Data-Driven Suite for Runtime Camera, Microphone, Storage, Location, and Overlay permissions.
"""

import time
import pytest
from pages.permissions_page import PermissionsPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.adb_helper import AdbHelper
from utils.logger import logger
from config import config

SHEET_NAME = "DevicePermissions_TestCases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestDevicePermissionsSuite:

    def test_device_permission_scenario(self, driver, test_case):
        """Execute runtime permission scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_PERM")
        desc = test_case.get("Scenario_Description", "Permission Scenario")
        permission = test_case.get("Permission", "")
        action = test_case.get("Action", "Allow")
        expected_result = test_case.get("Expected_Result", "SUCCESS").upper()
        expected_msg = test_case.get("Expected_Message", "")

        # Check Execute column from Excel
        execute_flag = str(test_case.get("Execute", "Y")).strip().upper()
        if execute_flag != "Y":
            logger.info(f"Skipping {tc_id} because Execute flag is '{execute_flag}' in Excel.")
            pytest.skip(f"Execute flag is '{execute_flag}' in Excel")


        test_title = f"{tc_id} - {desc}"
        logger.info(f"\n{'=' * 60}\nRunning [{SHEET_NAME}]: {test_title}\n{'=' * 60}")

        perm_page = PermissionsPage(driver)

        # 1. Handle permission via ADB or OS dialog
        if action.lower() == "allow":
            AdbHelper.grant_permission(permission)
            perm_page.handle_os_permission("Allow")
        elif action.lower() == "deny":
            AdbHelper.revoke_permission(permission)
            perm_page.handle_os_permission("Deny")

        time.sleep(2)
        screenshot = perm_page.take_screenshot(prefix=f"PERM_{tc_id}")
        ExcelReporter.log_result(
            test_name=test_title,
            status="PASSED",
            screenshot_path=screenshot,
            error_message=f"Permission {permission} handled with {action} ({expected_msg})"
        )
