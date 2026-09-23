"""
Logging utility for the Plutomen Connect test framework.
Outputs formatted logs to both console and a daily/session log file.
"""

import logging
import sys
from datetime import datetime
from config.config import LOGS_DIR


def setup_logger(name: str = "ConnectTest") -> logging.Logger:
    """Configure and return a standardized logger."""
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    log_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # File Handler
    log_filename = LOGS_DIR / f"run_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger


# Global default logger instance
logger = setup_logger()
