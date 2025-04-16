"""Logger setup for Stock-Tech-MovAvg module.
"""

import logging
import os
import sys

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "stock-tech-movavg.log")


def setup_logger():
    """Sets up a logger for the application with console and file handlers.

    :return: Configured logger instance
    """
    # Ensure logs directory exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logger = logging.getLogger("stock-tech-movavg")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
