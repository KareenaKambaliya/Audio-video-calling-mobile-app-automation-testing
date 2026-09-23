"""
Plutomen Connect - Mobile Automation Runner.
Opens the app on physical Android device and performs login or sheet execution.
Supports reading test credentials and scenarios from Excel (data/testcase_data.xlsx).

Usage:
    python open_app.py                      # Runs primary test case from Excel
    python open_app.py --from-excel         # Runs all active test cases from Excel sequentially
    python open_app.py --sheet Login        # Runs specific sheet suite via pytest
    python open_app.py --all-sheets         # Runs all 24 sheet suites via pytest
    python open_app.py --email u --password p # Custom credentials
"""

import argparse
import subprocess
import time
import traceback
import sys

from config import config
from core.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.home_page import HomePage
from utils.logger import logger
from utils.excel_reporter import ExcelReporter
from utils.excel_reader import get_login_test_cases, get_primary_credentials


def run_single_login(email: str, password: str, tc_id: str = "MANUAL", scenario: str = "Single Login"):
    """Execute login with given credentials and record results."""
    test_title = f"{tc_id} - {scenario}"

    print("\n" + "=" * 65)
    print(f"      PLUTOMEN CONNECT - {test_title.upper()}")
    print("=" * 65)
    print(f" Device UDID   : {config.DEVICE_UDID} ({config.DEVICE_NAME})")
    print(f" Login Account : {email}")
    print("=" * 65 + "\n")

    driver = None
    login_page = None
    try:
        logger.info("Initializing Appium driver session...")
        driver = DriverFactory.create_driver(auto_start_server=True)
        try:
            driver.activate_app(config.APP_PACKAGE)
        except Exception:
            pass
        login_page = LoginPage(driver)
        home_page = HomePage(driver)

        # Allow splash screen animation to settle
        logger.info("Waiting for app splash screen...")
        time.sleep(3)

        # Dismiss any initial blocking popups
        login_page.dismiss_initial_dialogs()

        # Execute Login
        logger.info(f"Submitting credentials for '{email}'...")
        login_page.login(email=email, password=password)

        time.sleep(4)
        screenshot = login_page.take_screenshot(prefix=f"RESULT_{tc_id}")

        # Log Success to Excel Report
        report_file = ExcelReporter.log_result(
            test_name=test_title,
            status="PASSED",
            screenshot_path=screenshot,
            error_message="App opened and login submitted successfully."
        )

        print("\n" + "=" * 65)
        print(f"  SUCCESS: {test_title} executed successfully!")
        print(f"  Screenshot   : {screenshot}")
        print(f"  Excel Report : {report_file}")
        print("=" * 65 + "\n")

    except Exception as e:
        lines = [line.strip() for line in str(e).split("\n") if line.strip() and line.strip() != "Message:"]
        summary = lines[0] if lines else str(e)
        error_msg = f"{e.__class__.__name__}: {summary}"[:200]
        tb_text = traceback.format_exc()
        logger.error(f"Execution error on {tc_id}: {error_msg}")

        screenshot_path = ""
        if driver is not None and login_page is not None:
            try:
                screenshot_path = login_page.take_screenshot(prefix=f"ERROR_{tc_id}")
            except Exception:
                pass

        report_file = ExcelReporter.log_result(
            test_name=test_title,
            status="FAILED",
            error_message=error_msg,
            screenshot_path=screenshot_path,
            traceback_text=tb_text
        )

        print("\n" + "!" * 65)
        print(f"  TEST FAILED: {test_title}")
        print(f"  Error        : {error_msg}")
        print(f"  Screenshot   : {screenshot_path}")
        print(f"  Excel Report : {report_file}")
        print("!" * 65 + "\n")

    finally:
        if driver is not None:
            logger.info("Closing driver session...")
            try:
                driver.quit()
            except Exception:
                pass


def run_all_from_excel():
    """Iterate through all enabled test cases in Excel and execute them."""
    test_cases = get_login_test_cases(only_enabled=True)
    if not test_cases:
        logger.warning("No active test cases found in Excel (Execute == 'Y').")
        return

    print("\n" + "#" * 65)
    print(f"  RUNNING {len(test_cases)} DATA-DRIVEN TEST CASES FROM EXCEL")
    print("#" * 65)

    for idx, tc in enumerate(test_cases, start=1):
        print(f"\n>>> [{idx}/{len(test_cases)}] Executing: {tc['TC_ID']} - {tc['Scenario_Description']}")
        run_single_login(
            email=tc.get("Email", ""),
            password=tc.get("Password", ""),
            tc_id=tc.get("TC_ID", f"TC_{idx}"),
            scenario=tc.get("Scenario_Description", "Login")
        )
        time.sleep(2)


def run_sheet_via_pytest(sheet_name: str = None):
    """Run pytest targeting a specific sheet or all sheets."""
    sheet_map = {
        "login": "tests/test_01_login.py",
        "call": "tests/test_02_create_call.py",
        "register": "tests/test_03_register.py",
        "forgot": "tests/test_04_forgot_password.py",
        "guest": "tests/test_05_guest_login.py",
        "webjoin": "tests/test_06_webjoin_deeplink.py",
        "receive": "tests/test_07_receive_call.py",
        "screenshare": "tests/test_08_screen_share.py",
        "network": "tests/test_09_call_network.py",
        "info": "tests/test_10_call_info.py",
        "schedule": "tests/test_11_create_schedule.py",
        "joining": "tests/test_12_schedule_joining.py",
        "details": "tests/test_13_schedule_details.py",
        "offline": "tests/test_14_schedule_offline.py",
        "chat": "tests/test_15_chat.py",
        "group": "tests/test_16_group_chat.py",
        "share": "tests/test_17_share_into_app.py",
        "gallery": "tests/test_18_gallery_media.py",
        "push": "tests/test_19_push_notification.py",
        "notification": "tests/test_20_notification_center.py",
        "boot": "tests/test_21_boot_persistence.py",
        "perm": "tests/test_22_device_permissions.py",
        "manage_perm": "tests/test_23_manage_permissions.py",
        "session": "tests/test_24_session_details.py",
    }

    target = "tests/"
    if sheet_name:
        key = sheet_name.lower().replace("_", "")
        for k, v in sheet_map.items():
            if k in key or key in k:
                target = v
                break
        else:
            target = f"tests/test_{sheet_name}.py"

    cmd = [sys.executable, "-m", "pytest", "-v", target]
    print(f"\nRunning command: {' '.join(cmd)}\n")
    subprocess.run(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plutomen Connect Automation Runner")
    parser.add_argument("--from-excel", action="store_true", help="Run all enabled test cases from Excel")
    parser.add_argument("--sheet", type=str, default=None, help="Run specific sheet test suite (e.g. login, register, call, chat)")
    parser.add_argument("--all-sheets", action="store_true", help="Run all 24 sheets via pytest")
    parser.add_argument("--email", type=str, default=None, help="User email / username")
    parser.add_argument("--password", type=str, default=None, help="User password")
    args = parser.parse_args()

    if args.all_sheets:
        run_sheet_via_pytest()
    elif args.sheet:
        run_sheet_via_pytest(args.sheet)
    elif args.from_excel:
        run_all_from_excel()
    else:
        excel_email, excel_pass = get_primary_credentials()
        final_email = args.email or excel_email
        final_pass = args.password or excel_pass

        run_single_login(
            email=final_email,
            password=final_pass,
            tc_id="TC_LOGIN_01",
            scenario="Excel Primary Login"
        )
