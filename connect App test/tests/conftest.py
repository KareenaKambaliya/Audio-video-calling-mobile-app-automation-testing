"""
Pytest configuration and shared fixtures for Plutomen Connect test suite.
Includes driver lifecycle, automatic failure screenshots, and Excel test reporting.
"""

import pytest
from core.driver_factory import DriverFactory
from utils.logger import logger
from utils.excel_reporter import ExcelReporter
from config import config


@pytest.fixture(scope="session", autouse=True)
def appium_server():
    """Ensure Appium server is alive before any tests run."""
    if not DriverFactory.is_server_running():
        logger.info("Appium server not detected. Starting local server...")
        DriverFactory.start_server()


@pytest.fixture(scope="function")
def driver(request):
    """
    Creates an Appium WebDriver instance for a test function.
    Automatically captures a screenshot and logs to Excel on failure.
    """
    app_driver = DriverFactory.create_driver(auto_start_server=False)
    yield app_driver

    # Handle test outcome
    test_name = request.node.name
    rep_call = getattr(request.node, "rep_call", None)

    if rep_call and rep_call.failed:
        screenshot_path = config.SCREENSHOTS_DIR / f"FAILURE_{test_name}.png"
        try:
            app_driver.save_screenshot(str(screenshot_path))
            logger.error(f"Test failed! Screenshot saved to: {screenshot_path}")
        except Exception as e:
            screenshot_path = ""
            logger.warning(f"Could not capture screenshot on failure: {e}")

        # Extract failure message
        error_msg = str(rep_call.longrepr) if rep_call.longrepr else "Test assertion or step failed."
        first_line_error = error_msg.split("\n")[-1] if "\n" in error_msg else error_msg

        # Log failure to Excel
        ExcelReporter.log_result(
            test_name=test_name,
            status="FAILED",
            error_message=first_line_error[:200],
            screenshot_path=str(screenshot_path) if screenshot_path else "",
            traceback_text=str(error_msg)[:1000]
        )
    elif rep_call and rep_call.passed:
        # Log pass to Excel
        ExcelReporter.log_result(
            test_name=test_name,
            status="PASSED",
            error_message="Test passed successfully."
        )
    elif rep_call and rep_call.skipped:
        # Log skip to Excel
        ExcelReporter.log_result(
            test_name=test_name,
            status="SKIPPED",
            error_message="Test skipped: Execute flag is 'N' in Excel."
        )

    # Teardown
    try:
        app_driver.quit()
        logger.info("Driver session terminated cleanly.")
    except Exception:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test execution status for failure screenshots and Excel reporting."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
