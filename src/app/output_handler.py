"""Module to handle output of moving average analysis to various targets.
"""

import json
from typing import Any

from .logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def send_to_output(data: dict[str, Any]) -> None:
    """Outputs processed moving average analysis to a chosen output target.

    Args:
    ----
        data (dict[str, Any]): The processed moving average analysis data.

    Returns:
    -------
        None

    """
    try:
        # Convert to JSON for output
        formatted_output: str = json.dumps(data, indent=4)

        # Log the output
        logger.info("Sending data to output: \n%s", formatted_output)

        # TODO: Replace this with actual output target (e.g., database, cloud storage)
        print(formatted_output)

    except Exception as e:
        logger.error("Failed to send output: %s", e)
