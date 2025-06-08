"""Main entry point for Stock-Tech-MovAvg.

This script consumes stock data from the queue, applies moving average
analysis, and publishes the results back to the output queue.
"""

import os
import sys

# Ensure src/ is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.setup_logger import setup_logger
from app.queue_handler import consume_messages

# Initialize logger
logger = setup_logger(__name__)


def main() -> None:
    """Entry point of the Moving Average Analysis Service.

    This function starts the service to consume stock data messages from the configured
    queue, process the data using the selected moving average technique, and publish the
    results.

    Args:
    ----



    """
    logger.info("Starting Moving Average Analysis Service...")
    consume_messages()


if __name__ == "__main__":
    main()
