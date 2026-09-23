"""
ADB Helper Module for Plutomen Connect Automation.
Executes device/OS-level operations (deep links, network toggles, permissions, broadcasts, app lifecycle) via ADB.
"""

import subprocess
import time
from config import config
from utils.logger import logger


class AdbHelper:
    """Helper methods executing ADB commands on the connected test device."""

    @staticmethod
    def _run_adb(args: list[str]) -> str:
        """Run an adb command with the configured device UDID."""
        cmd = ["adb"]
        if config.DEVICE_UDID:
            cmd.extend(["-s", config.DEVICE_UDID])
        cmd.extend(args)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15,
                check=False
            )
            out = (result.stdout or "").strip()
            err = (result.stderr or "").strip()
            if err and result.returncode != 0:
                logger.warning(f"ADB command {' '.join(cmd)} returned error: {err}")
            return out
        except Exception as e:
            logger.error(f"Failed to execute ADB command {' '.join(cmd)}: {e}")
            return ""

    @classmethod
    def launch_deep_link(cls, uri: str) -> bool:
        """Launch the app via a deep-link URI."""
        logger.info(f"Launching deep-link URI via ADB: {uri}")
        out = cls._run_adb(["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", uri])
        return "Error" not in out

    @classmethod
    def send_boot_completed(cls, package: str = config.APP_PACKAGE) -> bool:
        """Simulate device reboot by sending BOOT_COMPLETED broadcast."""
        logger.info(f"Sending BOOT_COMPLETED broadcast to {package} via ADB...")
        out = cls._run_adb(["shell", "am", "broadcast", "-a", "android.intent.action.BOOT_COMPLETED", "-p", package])
        return "result=0" in out or "Broadcast completed" in out

    @classmethod
    def set_wifi(cls, enable: bool):
        """Enable or disable Wi-Fi on device."""
        action = "enable" if enable else "disable"
        logger.info(f"Setting Wi-Fi to {action} via ADB...")
        cls._run_adb(["shell", "svc", "wifi", action])
        time.sleep(2)

    @classmethod
    def set_mobile_data(cls, enable: bool):
        """Enable or disable Mobile Data on device."""
        action = "enable" if enable else "disable"
        logger.info(f"Setting Mobile Data to {action} via ADB...")
        cls._run_adb(["shell", "svc", "data", action])
        time.sleep(2)

    @classmethod
    def set_airplane_mode(cls, enable: bool):
        """Toggle Airplane Mode on device."""
        val = "1" if enable else "0"
        logger.info(f"Setting Airplane mode to {val} via ADB...")
        cls._run_adb(["shell", "cmd", "connectivity", "airplane-mode", "enable" if enable else "disable"])
        time.sleep(2)

    @classmethod
    def force_stop_app(cls, package: str = config.APP_PACKAGE):
        """Kill the application process."""
        logger.info(f"Force stopping {package} via ADB...")
        cls._run_adb(["shell", "am", "force-stop", package])
        time.sleep(1)

    @classmethod
    def is_app_running(cls, package: str = config.APP_PACKAGE) -> bool:
        """Check whether app process is currently active."""
        out = cls._run_adb(["shell", "pidof", package])
        return bool(out.strip())

    @classmethod
    def open_app_settings(cls, package: str = config.APP_PACKAGE):
        """Open system application settings for package."""
        logger.info(f"Opening system app settings for {package} via ADB...")
        cls._run_adb(["shell", "am", "start", "-a", "android.settings.APPLICATION_DETAILS_SETTINGS", f"package:{package}"])
        time.sleep(2)

    @classmethod
    def grant_permission(cls, permission: str, package: str = config.APP_PACKAGE):
        """Grant a runtime permission via ADB."""
        perm = permission if permission.startswith("android.permission.") else f"android.permission.{permission.upper()}"
        logger.info(f"Granting {perm} to {package} via ADB...")
        cls._run_adb(["shell", "pm", "grant", package, perm])

    @classmethod
    def revoke_permission(cls, permission: str, package: str = config.APP_PACKAGE):
        """Revoke a runtime permission via ADB."""
        perm = permission if permission.startswith("android.permission.") else f"android.permission.{permission.upper()}"
        logger.info(f"Revoking {perm} from {package} via ADB...")
        cls._run_adb(["shell", "pm", "revoke", package, perm])

    @classmethod
    def send_share_intent(cls, text: str, package: str = config.APP_PACKAGE) -> bool:
        """Simulate external app sharing text into Plutomen Connect."""
        logger.info(f"Sending share intent text '{text}' via ADB...")
        out = cls._run_adb([
            "shell", "am", "start",
            "-a", "android.intent.action.SEND",
            "-t", "text/plain",
            "--es", "android.intent.extra.TEXT", text,
            "-p", package
        ])
        return "Error" not in out
