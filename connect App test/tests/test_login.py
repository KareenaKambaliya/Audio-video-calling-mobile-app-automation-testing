"""
Test cases for launching Plutomen Connect and verifying login workflow.
Execute: pytest -v tests/test_login.py
"""

import time
import pytest
from pages.login_page import LoginPage
from config import config
from utils.logger import logger


@pytest.mark.smoke
class TestLogin:

    def test_open_app_and_login(self, driver):
        """Verify opening the application and submitting login credentials."""
        logger.info("Starting test: test_open_app_and_login")
        login_page = LoginPage(driver)

        # Allow splash screen transition
        time.sleep(3)

        # Execute login
        login_page.login(email=config.LOGIN_EMAIL, password=config.LOGIN_PASSWORD)

        # Wait for transition post-login
        time.sleep(5)

        logger.info("Completed test: test_open_app_and_login")
