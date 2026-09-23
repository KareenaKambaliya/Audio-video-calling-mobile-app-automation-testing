"""
Excel Reporter Module.
Logs test results, timestamps, error messages, and clickable screenshot links to an Excel workbook.
"""

import os
import traceback
from datetime import datetime
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from config import config
from utils.logger import logger

REPORT_PATH = config.REPORTS_DIR / "Execution_Report.xlsx"


class ExcelReporter:
    """Manages appending test execution records to an Excel report."""

    HEADERS = [
        "#",
        "Timestamp",
        "Test / Action Name",
        "Status",
        "Error Message",
        "Screenshot File",
        "Traceback / Log"
    ]

    @classmethod
    def _get_or_create_workbook(cls) -> tuple[openpyxl.Workbook, openpyxl.worksheet.worksheet.Worksheet]:
        """Load existing workbook or create a new one with styled headers."""
        if REPORT_PATH.exists():
            try:
                wb = openpyxl.load_workbook(REPORT_PATH)
                ws = wb.active
                return wb, ws
            except Exception as e:
                logger.warning(f"Could not open existing report ({e}), creating a fresh workbook.")

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Test Execution Results"

        # Apply Header Styling
        header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")  # Navy Blue
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

        ws.append(cls.HEADERS)
        ws.row_dimensions[1].height = 28

        thin_border = Border(
            left=Side(style='thin', color='D9D9D9'),
            right=Side(style='thin', color='D9D9D9'),
            top=Side(style='thin', color='D9D9D9'),
            bottom=Side(style='thin', color='D9D9D9')
        )

        for col_num in range(1, len(cls.HEADERS) + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = center_align
            cell.border = thin_border

        return wb, ws

    @classmethod
    def log_result(
        cls,
        test_name: str,
        status: str,
        error_message: str = "",
        screenshot_path: str = "",
        traceback_text: str = ""
    ) -> str:
        """
        Log an execution entry with timestamp, status, error, and screenshot link to Excel.
        
        :param test_name: Name of the test scenario or step
        :param status: "PASSED", "FAILED", or "ERROR"
        :param error_message: Error description or exception message
        :param screenshot_path: Filepath of the captured screenshot
        :param traceback_text: Detailed exception traceback
        :return: Path of saved Excel report
        """
        wb, ws = cls._get_or_create_workbook()

        row_idx = ws.max_row + 1
        record_id = row_idx - 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        status_upper = status.upper()
        if "FAIL" in status_upper or "ERR" in status_upper:
            status_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")  # Soft Red
            status_font = Font(name="Calibri", size=10, bold=True, color="C00000")
        else:
            status_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")  # Soft Green
            status_font = Font(name="Calibri", size=10, bold=True, color="375623")

        regular_font = Font(name="Calibri", size=10)
        link_font = Font(name="Calibri", size=10, color="0563C1", underline="single")
        left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)
        center_align = Alignment(horizontal="center", vertical="center")

        thin_border = Border(
            left=Side(style='thin', color='E0E0E0'),
            right=Side(style='thin', color='E0E0E0'),
            top=Side(style='thin', color='E0E0E0'),
            bottom=Side(style='thin', color='E0E0E0')
        )

        ws.cell(row=row_idx, column=1, value=record_id).alignment = center_align
        ws.cell(row=row_idx, column=2, value=timestamp).alignment = center_align
        ws.cell(row=row_idx, column=3, value=test_name).alignment = left_align

        # Status cell
        c_status = ws.cell(row=row_idx, column=4, value=status_upper)
        c_status.fill = status_fill
        c_status.font = status_font
        c_status.alignment = center_align

        # Error Message
        ws.cell(row=row_idx, column=5, value=error_message or "-").alignment = left_align

        # Screenshot Cell with clickable hyperlink
        c_shot = ws.cell(row=row_idx, column=6)
        if screenshot_path and os.path.exists(screenshot_path):
            screenshot_name = Path(screenshot_path).name
            c_shot.value = screenshot_name
            c_shot.hyperlink = str(Path(screenshot_path).resolve())
            c_shot.font = link_font
            c_shot.alignment = left_align
        else:
            c_shot.value = "-"
            c_shot.alignment = center_align

        # Traceback / Log
        ws.cell(row=row_idx, column=7, value=traceback_text or "-").alignment = left_align

        # Apply borders & font to all cells in the row
        for col in range(1, len(cls.HEADERS) + 1):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = thin_border
            if col not in [4, 6]:  # Skip status & link fonts
                cell.font = regular_font

        ws.row_dimensions[row_idx].height = 24

        # Auto-fit column widths
        col_widths = {1: 6, 2: 20, 3: 25, 4: 12, 5: 35, 6: 28, 7: 40}
        for col_idx, width in col_widths.items():
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = width

        # Save workbook (handles potential permission lock if user has file open in Excel)
        target_file = REPORT_PATH
        try:
            wb.save(target_file)
        except PermissionError:
            alt_name = f"Execution_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            target_file = config.REPORTS_DIR / alt_name
            wb.save(target_file)
            logger.warning(f"Default report file locked by another program. Saved to: {target_file}")

        logger.info(f"Excel Report updated: {target_file.name} (Row {row_idx})")
        return str(target_file)
