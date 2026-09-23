"""
DriverFactory handles Appium server lifecycle and Appium WebDriver instance creation.
"""

import os
import time
import socket
import subprocess
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config import config
from utils.logger import logger


class DriverFactory:
    """Manages Appium server availability and WebDriver instantiation."""

    @staticmethod
    def is_server_running(host: str = config.APPIUM_HOST, port: int = config.APPIUM_PORT) -> bool:
        """Check if an Appium server is actively listening on configured port."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)
            return s.connect_ex((host, port)) == 0

    @classmethod
    def start_server(cls) -> subprocess.Popen:
        """Start Appium server in background if not already alive."""
        import sys
        logger.info(f"Starting local Appium server at {config.APPIUM_SERVER_URL}...")
        server_log_file = config.LOGS_DIR / "appium_server.log"
        appium_cmd = "appium.cmd" if sys.platform == "win32" else "appium"
        
        env = os.environ.copy()
        env["ANDROID_HOME"] = r"C:\Users\baps\AppData\Local\Android\Sdk"
        env["ANDROID_SDK_ROOT"] = r"C:\Users\baps\AppData\Local\Android\Sdk"
        env["PATH"] = r"C:\Users\baps\AppData\Local\Android\Sdk\platform-tools;" + env.get("PATH", "")

        log_f = open(server_log_file, "a", encoding="utf-8")
        try:
            proc = subprocess.Popen(
                f"{appium_cmd} --port {config.APPIUM_PORT} --relaxed-security",
                stdout=log_f,
                stderr=log_f,
                env=env,
                shell=True
            )
        except Exception as e:
            logger.error(f"Failed to launch Appium process: {e}")
            raise

        # Poll until server becomes responsive
        timeout = 25
        start_time = time.time()
        while time.time() - start_time < timeout:
            if cls.is_server_running():
                logger.info(f"Appium server is UP and accepting connections (logs: {server_log_file.name}).")
                return proc
            time.sleep(1)

        logger.warning(
            f"Appium server did not become responsive on port {config.APPIUM_PORT} within {timeout}s. "
            "If connections fail, start Appium manually: 'appium --port 4723 --relaxed-security'"
        )
        return proc

    @classmethod
    def get_capabilities(cls) -> UiAutomator2Options:
        """Build and return UiAutomator2 capabilities."""
        options = UiAutomator2Options()
        options.platform_name = config.PLATFORM_NAME
        options.automation_name = config.AUTOMATION_NAME
        options.device_name = config.DEVICE_NAME
        options.udid = config.DEVICE_UDID
        options.platform_version = config.PLATFORM_VERSION
        options.app_package = config.APP_PACKAGE
        options.app_activity = config.APP_ACTIVITY
        options.app_wait_activity = config.APP_WAIT_ACTIVITY
        options.no_reset = config.NO_RESET
        options.auto_grant_permissions = config.AUTO_GRANT_PERMISSIONS
        options.new_command_timeout = config.NEW_COMMAND_TIMEOUT

        # Explicit path to adb executable
        if hasattr(config, "ADB_PATH") and os.path.exists(config.ADB_PATH):
            options.set_capability("appium:adbExec", config.ADB_PATH)

        return options

    @classmethod
    def create_driver(cls, auto_start_server: bool = True) -> webdriver.Remote:
        """Initialize and return an active Appium WebDriver instance."""
        if auto_start_server and not cls.is_server_running():
            cls.start_server()

        logger.info(f"Connecting to Appium at {config.APPIUM_SERVER_URL} (Device: {config.DEVICE_UDID})...")
        options = cls.get_capabilities()
        driver = webdriver.Remote(
            command_executor=config.APPIUM_SERVER_URL,
            options=options
        )
        driver.implicitly_wait(config.IMPLICIT_WAIT_TIMEOUT)
        logger.info(f"Appium session created! Session ID: {driver.session_id}")
        return driver
