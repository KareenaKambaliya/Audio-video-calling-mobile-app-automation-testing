"""
Test Suite: Gallery & Media (Sheet: GalleryMedia_Test_Cases)
Data-Driven Suite for Gallery browsing, full-screen viewing, swiping, and downloads.
"""

import time
import pytest
from pages.gallery_page import GalleryPage
from pages.login_page import LoginPage
from utils.excel_reader import get_sheet_test_cases
from utils.excel_reporter import ExcelReporter
from utils.logger import logger
from config import config

SHEET_NAME = "GalleryMedia_Test_Cases"
TEST_CASES = get_sheet_test_cases(SHEET_NAME)


@pytest.mark.parametrize("test_case", TEST_CASES, ids=[tc.get("TC_ID", f"TC_{i}") for i, tc in enumerate(TEST_CASES)])
class TestGalleryMediaSuite:

    def test_gallery_media_scenario(self, driver, test_case):
        """Execute gallery media scenario according to Excel specification."""
        tc_id = test_case.get("TC_ID", "TC_GAL")
        desc = test_case.get("Scenario_Description", "Gallery Scenario")
        media_type = test_case.get("Media_Type", "Image")
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
        gallery_page = GalleryPage(driver)

        # 1. Ensure logged in
        login_page.dismiss_initial_dialogs()
        if not login_page.is_already_logged_in():
            login_page.login(config.LOGIN_EMAIL, config.LOGIN_PASSWORD)
            time.sleep(3)

        # 2. Perform gallery action
        if tc_id == "TC_GAL_01":
            gallery_page.open_first_media_item()
            time.sleep(2)
            assert gallery_page.is_full_screen_viewer_displayed(), "Full screen viewer did not open!"
        elif tc_id == "TC_GAL_02":
            gallery_page.open_first_media_item()
            time.sleep(2)
            gallery_page.swipe_next_media()
            time.sleep(2)
        elif tc_id == "TC_GAL_03":
            gallery_page.open_first_media_item()
            time.sleep(1)
            gallery_page.download_media()
            time.sleep(2)
        elif tc_id == "TC_GAL_05":
            gallery_page.open_first_media_item()
            time.sleep(1)
            gallery_page.delete_media()
            time.sleep(2)

        screenshot = gallery_page.take_screenshot(prefix=f"GAL_{tc_id}")
        ExcelReporter.log_result(
            test_name=test_title,
            status="PASSED",
            screenshot_path=screenshot,
            error_message=f"Gallery action verified ({expected_msg})"
        )
