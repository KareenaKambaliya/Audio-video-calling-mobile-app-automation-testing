"""
Central Configuration Module for Plutomen Connect Automation Framework.
Handles device detection, capabilities, environment variables, paths, and test data.
"""

import os
import subprocess
from pathlib import Path

# --- Project Paths ---
ROOT_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = ROOT_DIR / "screenshots"
REPORTS_DIR = ROOT_DIR / "reports"
LOGS_DIR = ROOT_DIR / "reports" / "logs"

SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# --- Ensure Environment Variables (Java, Android SDK, ADB) ---
if not os.environ.get("JAVA_HOME") or "<path" in os.environ.get("JAVA_HOME", ""):
    default_jdk = r"C:\Program Files\Java\jdk-21.0.12.1"
    if os.path.exists(default_jdk):
        os.environ["JAVA_HOME"] = default_jdk

if not os.environ.get("ANDROID_HOME"):
    default_sdk = r"C:\Users\baps\AppData\Local\Android\Sdk"
    if os.path.exists(default_sdk):
        os.environ["ANDROID_HOME"] = default_sdk
        os.environ["ANDROID_SDK_ROOT"] = default_sdk

# Add platform-tools to PATH
ADB_PATH = r"C:\Users\baps\AppData\Local\Android\Sdk\platform-tools\adb.exe"
for candidate in [r"C:\Users\baps\AppData\Local\Android\Sdk\platform-tools", r"C:\platform-tools"]:
    if os.path.exists(candidate) and candidate not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{candidate};" + os.environ.get("PATH", "")


def get_connected_device_udid() -> str:
    """Auto-detect connected Android device UDID via adb."""
    try:
        output = subprocess.check_output(["adb", "devices"], text=True)
        lines = [line.strip() for line in output.strip().split("\n")[1:] if line.strip()]
        for line in lines:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                return parts[0]
    except Exception:
        pass
    return "10BF782BCA007C3"


# --- Appium Server Settings ---
APPIUM_HOST = os.environ.get("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = int(os.environ.get("APPIUM_PORT", 4723))
APPIUM_SERVER_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"

# --- Mobile Device Capabilities ---
DEVICE_UDID = get_connected_device_udid()
DEVICE_NAME = os.environ.get("DEVICE_NAME", "Vivo_V2427")
PLATFORM_NAME = "Android"
PLATFORM_VERSION = os.environ.get("PLATFORM_VERSION", "16")
AUTOMATION_NAME = "UiAutomator2"

# --- Target Application (Plutomen Connect) ---
APP_PACKAGE = "com.plutomen.ARMS"
APP_ACTIVITY = "com.plutomen.ARMS.activity.SplashActivity"
APP_WAIT_ACTIVITY = "com.plutomen.ARMS.activity.HomeActivity,com.plutomen.ARMS.*"

# Session Flags
NO_RESET = True
AUTO_GRANT_PERMISSIONS = True
NEW_COMMAND_TIMEOUT = 300
IMPLICIT_WAIT_TIMEOUT = 0
EXPLICIT_WAIT_TIMEOUT = 15

# --- Test Data & Artifacts ---
TEST_DATA_FILE = ROOT_DIR / "data" / "testcase_data.xlsx"
APK_PATH = ROOT_DIR / "data" / "Connect_mobile_ss.apk"
DEEP_LINK_SCHEME = "plutomen-connect://app.pluto-men.com/join"

# --- Test Credentials ---
LOGIN_EMAIL = os.environ.get("CONNECT_EMAIL", "kareena.k@pluto-men.com")
LOGIN_PASSWORD = os.environ.get("CONNECT_PASSWORD", "Kareena@123")
