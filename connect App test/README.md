# Plutomen Connect - Mobile Automation Framework

A clean, modular, data-driven mobile automation testing framework for **Plutomen Connect** (`Connect_mobile_ss.apk` / `com.plutomen.ARMS`) on Android physical devices using **Python**, **Appium 3 (UiAutomator2)**, and **Pytest**.

---

## 📁 Framework Structure

```
c:\Kareena\connect App test\
├── config/
│   ├── __init__.py
│   └── config.py              # Capabilities, device auto-discovery, paths, default credentials
│
├── core/
│   ├── __init__.py
│   ├── driver_factory.py      # Appium server management & WebDriver lifecycle
│   └── base_page.py           # Core interactions (waits, clicks, typing, gestures, screenshots)
│
├── data/
│   ├── Connect_mobile_ss.apk  # 📱 Target application APK
│   ├── testcase_data.xlsx     # 📊 Excel workbook containing 24 sheets & 134 test scenarios
│   └── login_test_data.xlsx   # 📑 Original/legacy test data (preserved for backward compatibility)
│
├── pages/                     # 📄 Page Object Model layer
│   ├── __init__.py
│   ├── login_page.py          # Login screen, auth links & logout
│   ├── home_page.py           # Dashboard / Home screen
│   ├── register_page.py       # User Registration screen
│   ├── forgot_password_page.py# Forgot Password & reset
│   ├── guest_login_page.py    # Guest login & 9-digit join code
│   ├── webjoin_page.py        # Web join & deep link handling
│   ├── call_page.py           # 1-on-1 Audio/Video Call, receive & call info
│   ├── screenshare_page.py    # AR & Non-AR screen share, freeze & pen annotations
│   ├── schedule_page.py       # Create, join, details & cancel schedule
│   ├── offline_mode_page.py   # Self-mode offline sessions
│   ├── chat_page.py           # 1-on-1 Chat, text, media attachments
│   ├── group_chat_page.py     # Group creation, member add/remove, group messaging
│   ├── gallery_page.py        # Media viewer, swipe, download, zoom
│   ├── notification_page.py   # In-app alerts, notification center, shade
│   ├── permissions_page.py    # Manage permissions screen & OS dialogs
│   ├── session_details_page.py# Post-call summary & historical sessions
│   └── sharing_page.py        # Share intent handling from external apps
│
├── tests/                     # 🧪 24 Test Suites organized by sheet
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures & auto-failure screenshot hook
│   ├── test_login.py                  # Original single test suite (preserved)
│   ├── test_login_ddt.py              # Original DDT test suite (preserved)
│   ├── test_01_login.py               # Sheet: Login_Test_Cases (6 TCs)
│   ├── test_02_create_call.py         # Sheet: Create_Call_Test_Cases (6 TCs)
│   ├── test_03_register.py            # Sheet: Register_Test_Cases (7 TCs)
│   ├── test_04_forgot_password.py     # Sheet: ForgotPassword_Test_Cases (5 TCs)
│   ├── test_05_guest_login.py         # Sheet: GuestLogin_Test_Cases (5 TCs)
│   ├── test_06_webjoin_deeplink.py    # Sheet: WebJoinDeepLink_Test_Cases (4 TCs)
│   ├── test_07_receive_call.py        # Sheet: ReceiveCall_Test_Cases (7 TCs)
│   ├── test_08_screen_share.py        # Sheet: ScreenShare_Test_Cases (6 TCs)
│   ├── test_09_call_network.py        # Sheet: CallNetworkHandling_Test_Cases (5 TCs)
│   ├── test_10_call_info.py           # Sheet: CallInfo_Test_Cases (3 TCs)
│   ├── test_11_create_schedule.py     # Sheet: CreateSchedule_Test_Cases (8 TCs)
│   ├── test_12_schedule_joining.py    # Sheet: ScheduleCallJoining_Test_Cases (6 TCs)
│   ├── test_13_schedule_details.py    # Sheet: ScheduleCallDetails_Test_Cases (4 TCs)
│   ├── test_14_schedule_offline.py    # Sheet: ScheduleOfflineMode_TestCases (5 TCs)
│   ├── test_15_chat.py                # Sheet: Chat_Test_Cases (7 TCs)
│   ├── test_16_group_chat.py          # Sheet: GroupChat_Test_Cases (8 TCs)
│   ├── test_17_share_into_app.py      # Sheet: ShareIntoApp_Test_Cases (4 TCs)
│   ├── test_18_gallery_media.py       # Sheet: GalleryMedia_Test_Cases (5 TCs)
│   ├── test_19_push_notification.py   # Sheet: PushNotification_TestCases (6 TCs)
│   ├── test_20_notification_center.py # Sheet: NotificationCenter_TestCases (5 TCs)
│   ├── test_21_boot_persistence.py    # Sheet: BootPersistence_TestCases (3 TCs)
│   ├── test_22_device_permissions.py  # Sheet: DevicePermissions_TestCases (10 TCs)
│   ├── test_23_manage_permissions.py  # Sheet: ManagePermissionScr_TestCases (3 TCs)
│   └── test_24_session_details.py     # Sheet: SessionDetails_TestCases (6 TCs)
│
├── utils/
│   ├── __init__.py
│   ├── excel_reader.py        # Dynamic parser for all sheets in testcase_data.xlsx
│   ├── excel_reporter.py      # Logs results, timestamps & clickable screenshot links
│   ├── adb_helper.py          # ADB automation for network, intents, broadcasts, permissions
│   └── logger.py              # Centralized logging (console + daily log files)
│
├── reports/
│   ├── Execution_Report.xlsx  # 📈 Live Excel execution report with screenshots
│   └── logs/                  # Execution log files
│
├── screenshots/               # Captured screenshots
├── open_app.py                # Main executable test runner
├── pytest.ini                 # Pytest configuration
└── requirements.txt           # Dependencies
```

---

## 🔍 APK Code Analysis Summary (`Connect_mobile_ss.apk`)

The framework was built after comprehensive reverse-engineering of `Connect_mobile_ss.apk`:
- **Package Name**: `com.plutomen.ARMS`
- **Main Launch Activity**: `com.plutomen.ARMS.activity.SplashActivity`
- **Total Components Discovered**:
  - **261 XML Layouts** inspected
  - **24 DEX Files** analyzed
  - **8,077 Resource IDs** extracted and cataloged
  - **14,223 Localization Strings** indexed
- **Proprietary Plutomen UI Widgets Mapped**:
  - Custom Buttons: `com.plutomen.ARMS.utils.PtmButton`
  - Custom Inputs: `com.plutomen.ARMS.utils.PtmEditText`
  - Custom Text Views: `com.plutomen.ARMS.utils.PtmTextView`
  - Custom Headers: `com.plutomen.ARMS.utils.PtmHeader`
  - Custom Empty States: `com.plutomen.ARMS.utils.PtmNoData`
  - Custom Media Player: `com.plutomen.ARMS.utils.AndExoPlayerView`
- **Deep Linking Protocol**: Custom scheme `ptmconnect://` mapped in `AndroidManifest.xml` for direct call/meeting joining.

---

## 📊 24 Test Sheets in `data/testcase_data.xlsx`

| # | Sheet Name | Suite File | Test Count |
|---|---|---|:---:|
| 1 | `Login_Test_Cases` | `tests/test_01_login.py` | 6 |
| 2 | `Create_Call_Test_Cases` | `tests/test_02_create_call.py` | 6 |
| 3 | `Register_Test_Cases` | `tests/test_03_register.py` | 7 |
| 4 | `ForgotPassword_Test_Cases` | `tests/test_04_forgot_password.py` | 5 |
| 5 | `GuestLogin_Test_Cases` | `tests/test_05_guest_login.py` | 5 |
| 6 | `WebJoinDeepLink_Test_Cases` | `tests/test_06_webjoin_deeplink.py` | 4 |
| 7 | `ReceiveCall_Test_Cases` | `tests/test_07_receive_call.py` | 7 |
| 8 | `ScreenShare_Test_Cases` | `tests/test_08_screen_share.py` | 6 |
| 9 | `CallNetworkHandling_Test_Cases` | `tests/test_09_call_network.py` | 5 |
| 10 | `CallInfo_Test_Cases` | `tests/test_10_call_info.py` | 3 |
| 11 | `CreateSchedule_Test_Cases` | `tests/test_11_create_schedule.py` | 8 |
| 12 | `ScheduleCallJoining_Test_Cases` | `tests/test_12_schedule_joining.py` | 6 |
| 13 | `ScheduleCallDetails_Test_Cases` | `tests/test_13_schedule_details.py` | 4 |
| 14 | `ScheduleOfflineMode_TestCases` | `tests/test_14_schedule_offline.py` | 5 |
| 15 | `Chat_Test_Cases` | `tests/test_15_chat.py` | 7 |
| 16 | `GroupChat_Test_Cases` | `tests/test_16_group_chat.py` | 8 |
| 17 | `ShareIntoApp_Test_Cases` | `tests/test_17_share_into_app.py` | 4 |
| 18 | `GalleryMedia_Test_Cases` | `tests/test_18_gallery_media.py` | 5 |
| 19 | `PushNotification_TestCases` | `tests/test_19_push_notification.py` | 6 |
| 20 | `NotificationCenter_TestCases` | `tests/test_20_notification_center.py` | 5 |
| 21 | `BootPersistence_TestCases` | `tests/test_21_boot_persistence.py` | 3 |
| 22 | `DevicePermissions_TestCases` | `tests/test_22_device_permissions.py` | 10 |
| 23 | `ManagePermissionScr_TestCases` | `tests/test_23_manage_permissions.py` | 3 |
| 24 | `SessionDetails_TestCases` | `tests/test_24_session_details.py` | 6 |
| **Total** | **24 Sheets** | | **134 Test Cases** |

---

## ⚙️ Execution Flow & Excel Sheet Dynamics

### 1. Sequential Execution: Does it move to the next test case?
**YES, automatically.** The framework executes test cases sequentially one by one:
- **On Success (`PASSED`)**: The test verifies expected UI elements, logs the success, saves a confirmation screenshot in `screenshots/`, records `PASSED` in `reports/Execution_Report.xlsx`, and **immediately proceeds to the next test case**.
- **On Failure (`FAILED`)**: The test captures an error screenshot, logs the complete failure reason and stack trace in the Excel report, resets the app state if necessary, and **continues executing subsequent test cases without stopping the suite**.
- **On Skipped (`SKIPPED`)**: If a test case has `Execute: N`, pytest skips it in under 1 millisecond without launching Appium actions, logs `SKIPPED` in the report, and moves straight to the next test.

```
[Test 1] ───► (PASS / FAIL / SKIP) ───► Log to Excel & Screenshot
                                               │
                                               ▼
[Test 2] ◄────────────────────────────── State Teardown & Reset
   │
   ▼
 (PASS / FAIL / SKIP) ───► Log to Excel ───► [Test 3] ...
```

### 2. Execution Based on `Execute` Column (`Y` vs `N`)
**YES.** Every single test in all 24 test suites actively reads the `Execute` column from `data/testcase_data.xlsx`:
- **`Execute: Y`**: The test case will run on the physical device.
- **`Execute: N`**: The test case is bypassed with `pytest.skip(reason=...)`. No device actions or waits are wasted.
- You can enable or disable any specific test scenario at any time just by changing `Y` or `N` in Excel and saving the file.

### 3. Will Changing the Sequence of Test Cases in Excel Hamper the Script?
**NO, it will NOT hamper or break anything:**
1. **Dynamic Column & Row Resolution**: The parser (`utils/excel_reader.py`) reads data rows as dictionaries keyed by header names (`TC_ID`, `Scenario_Description`, `Email`, `Password`, `Expected_Result`, etc.). It does not depend on hardcoded row or column indexes.
2. **Autonomous Test Design**: Each test case is self-contained. It ensures the application is in the correct initial state before performing actions (e.g. logging out first if already logged in, returning to the Home screen, or dismissing transient OS dialogs).
3. **Flexible Sorting**: You can reorder rows, insert new rows, or re-arrange columns in Excel without altering any test code.

### 4. Were Existing Files Changed or Overwritten?
**NO.** All existing framework files have been preserved for full backward compatibility:
- Legacy test files (`tests/test_login.py`, `tests/test_login_ddt.py`) and legacy data (`data/login_test_data.xlsx`) remain intact and functional.
- All new suites for the 24 sheets were created as independent, modular suites: `tests/test_01_login.py` through `tests/test_24_session_details.py`.

---

## 📱 Attached Physical Device Setup & Testing

The framework is configured to run on your attached physical Android phone (**Vivo V2427**, UDID: `10BF782BCA007C3`, Android 16 / API 36).

### Pre-Run Setup:
1. **Verify ADB Connection**:
   ```powershell
   adb devices
   ```
   *Your device `10BF782BCA007C3` must be listed as `device`.*

2. **Keep Device Screen Awake (Crucial)**:
   Prevent the phone from going to sleep during automated testing:
   ```powershell
   adb shell svc power stayon true
   ```
   *(To revert after testing: `adb shell svc power stayon false`)*

3. **Start Appium Server**:
   ```powershell
   appium --port 4723 --relaxed-security
   ```
   *(The framework also includes automatic Appium background server auto-spawning in `core/driver_factory.py`).*

4. **SDK & ADB Path Handling**:
   The framework explicitly configures `appium:adbExec` pointing to `C:\Users\baps\AppData\Local\Android\Sdk\platform-tools\adb.exe` to prevent any path mismatches.

---

## 🚀 How to Run Test Cases

### Option 1: Run via Pytest (Recommended)

Run any specific sheet test suite:
```powershell
# Sheet 1: Login
python -m pytest -v tests/test_01_login.py

# Sheet 2: Create Call
python -m pytest -v tests/test_02_create_call.py

# Sheet 3: Register
python -m pytest -v tests/test_03_register.py

# Sheet 11: Create Schedule
python -m pytest -v tests/test_11_create_schedule.py

# Sheet 15: 1-on-1 Chat
python -m pytest -v tests/test_15_chat.py
```

Run a specific test case by its ID:
```powershell
python -m pytest -v tests/test_01_login.py -k TC_LOGIN_01
python -m pytest -v tests/test_03_register.py -k TC_REG_01
python -m pytest -v tests/test_11_create_schedule.py -k TC_SCH_01
```

Run all 24 sheets (134 test cases):
```powershell
python -m pytest -v
```

Check collected test cases across all 24 sheets without executing:
```powershell
python -m pytest --collect-only
```

---

### Option 2: Run via CLI Runner (`open_app.py`)

Run the primary active test case from Excel:
```powershell
python open_app.py
```

Run all active test cases from Excel in a continuous loop:
```powershell
python open_app.py --from-excel
```

Run a specific sheet by name:
```powershell
python open_app.py --sheet login
python open_app.py --sheet register
python open_app.py --sheet call
python open_app.py --sheet chat
```

Run all 24 sheets sequentially:
```powershell
python open_app.py --all-sheets
```

---

## 📈 Automatic Excel Reporting (`reports/Execution_Report.xlsx`)

Every test run automatically logs results into [`reports/Execution_Report.xlsx`](file:///c:/Kareena/connect%20App%20test/reports/Execution_Report.xlsx) with live styling:

| Column | Description |
|---|---|
| **Timestamp** | Date and exact time when the test finished execution |
| **Test Name** | Test Case ID and Scenario Description from Excel |
| **Status** | Color-coded: `PASSED` (Green), `FAILED` (Red), `SKIPPED` (Yellow) |
| **Error Message** | Outcome summary or assertion/exception stacktrace |
| **Screenshot Link** | Direct **clickable hyperlink** to open the captured screenshot image file |

---

## ❓ Frequently Asked Questions (FAQ)

### Q1: What happens if a test case succeeds? Will it move to the next test case?
> **Yes.** When a test case succeeds, pytest marks it as `PASSED`, saves a timestamped screenshot, writes the result to `reports/Execution_Report.xlsx`, and immediately triggers the next test case in sequence.

### Q2: What happens if a test case fails? Will the whole run stop?
> **No, the run continues.** If a test case fails, an error screenshot is taken and linked in the Excel report. The teardown routine resets the app to the initial state, and pytest proceeds to execute the remaining test cases.

### Q3: Does changing the order or sequence of rows in Excel affect execution?
> **No.** All test data is mapped dynamically by column header name (`TC_ID`, `Email`, etc.). Moving row 5 to row 2, or changing column order, will not hamper the scripts.

### Q4: How do I skip tests that I don't want to run?
> Open `data/testcase_data.xlsx`, find the test case, set the `Execute` column to `N`, and save. When you run pytest, that test case will be recorded as `SKIPPED` without taking up execution time on your phone.
